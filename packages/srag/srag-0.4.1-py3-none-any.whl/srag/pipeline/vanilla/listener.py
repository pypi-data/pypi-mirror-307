import time

import pydantic

from ..pipeline import BaseTransform, State, TransformListener


class TransformLog(pydantic.BaseModel):
    name: str
    created_at: float = pydantic.Field(default_factory=lambda: time.time())
    duration: float = 0.0
    state_before: State | None = None
    state_after: State | None = None

    def finish(self, state: State):
        self.duration = time.time() - self.created_at
        self.state_after = state


class PerfTracker(TransformListener):
    def __init__(
        self, print_state: bool = False, print_enter: bool = False, print_output: bool = False
    ) -> None:
        super().__init__()
        self._print_state = print_state
        self._print_enter = print_enter
        self._print_output = print_output
        self.time = []

    async def on_transform_enter(self, transform: BaseTransform, state):
        from pprint import pprint

        if self._print_enter:
            print(f"[Entering] - {transform.name}")
        if self._print_state:
            pprint(f"[State] - {state}")
        self.time.append(time.time())

    async def on_transform_exit(self, transform: BaseTransform, state):
        last_time = self.time.pop()
        if self._print_output and transform.output_key:
            keys = (
                [transform.output_key]
                if isinstance(transform.output_key, str)
                else transform.output_key
            )
            outputs = {key: state.get(key, None) for key in keys}
            output_text = ("-" * 20 + "\n").join([f"## {k}\n{v}" for k, v in outputs.items()])
            print(f"[Output] - {output_text}")
        print(f"[Exiting] - {transform.name}({time.time() - last_time:.2f}s used)")

    def __getattribute__(self, name: str):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            print(name)
            if name.startswith("on_") and name.endswith("_enter"):
                return self.on_transform_enter
            if name.startswith("on_") and name.endswith("_exit"):
                return self.on_transform_exit
            raise AttributeError


class PipelineMemoryStore(TransformListener):
    def __init__(self):
        self.logs = []

    async def on_transform_enter(self, transform: BaseTransform, state: State):
        self.logs.append(TransformLog(name=transform.name, state_before=state))

    async def on_transform_exit(self, transform: BaseTransform, state: State):
        self.logs[-1].finish(state)
