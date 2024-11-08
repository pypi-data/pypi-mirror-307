from dataclasses import dataclass
from typing import Awaitable, Callable, List, Union

from srag.document import BaseReranker, BaseRetriever, Chunk
from srag.llm.message import Message

from ..pipeline import BaseTransform, State


@dataclass
class LLMCost:
    total_tokens: int = 0
    total_cost: float = 0.0
    input_tokens: int = 0
    input_cost: float = 0.0
    output_tokens: int = 0
    output_cost: float = 0.0


class VanillaState(State):
    query: str
    doc_ids: List[str]
    rewritten_queries: List[str]
    history: Union[List[Message], str]
    chunks: List[Chunk]
    context: str
    final_prompt: str
    response: str
    cost: LLMCost


class VanillaTransform(BaseTransform[VanillaState]):
    pass


class TextProcessor(VanillaTransform):
    def __init__(self, fn_process: Callable[[str], Awaitable[str]], key: str):
        super().__init__(input_key=key, output_key=key)
        self.fn_process = fn_process
        self.key = key

    async def transform(self, state: VanillaState, **kwargs) -> VanillaState:
        state[self.key] = await self.fn_process(state[self.key])
        return state


class HistoryProcessor(VanillaTransform):
    def __init__(
        self,
        fn_process: Callable[[list[Message]], Awaitable[str]],
        input_key: str = "history",
        output_key: str = "history",
    ):
        super().__init__(input_key=input_key, output_key=output_key)
        self.fn_process = fn_process

    async def transform(self, state: VanillaState, **kwargs) -> VanillaState:
        state[self.output_key] = await self.fn_process(state.get(self.input_key))
        return state


class ContextComposer(VanillaTransform):
    def __init__(
        self,
        fn_process: Callable[[list[Chunk]], Awaitable[str]],
        input_key: str = "chunks",
        output_key: str = "context",
    ):
        super().__init__(input_key=input_key, output_key=output_key)
        self.fn_process = fn_process

    async def transform(self, state: VanillaState, **kwargs) -> VanillaState:
        state[self.output_key] = await self.fn_process(state.get(self.input_key))
        return state


class PromptComposer(VanillaTransform):
    def __init__(
        self,
        fn_process: Callable[[str, str, str], Awaitable[str]],
        input_key: list[str] = ["query", "context", "history"],
        output_key: str = "final_prompt",
    ):
        super().__init__(input_key=input_key, output_key=output_key)
        self.fn_process = fn_process

    async def transform(self, state: VanillaState, **kwargs) -> VanillaState:
        state[self.output_key] = await self.fn_process(**self._get_input(state))
        return state


class Generation(VanillaTransform):
    def __init__(
        self,
        llm_model: str,
        temperature: float = 0.01,
        top_p: float = 0.01,
        max_tokens: int | None = None,
        seed: int | None = None,
        input_key: str = "final_prompt",
        output_key: str = "response",
        cost_key: str = "cost",
    ):
        super().__init__(input_key=input_key, output_key=output_key)
        self.llm_model = llm_model
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.input_key = input_key
        self.cost_key = cost_key
        self.seed = seed

    def _prepare_chat_kwargs(self, state: VanillaState):
        chat_kwargs = {
            "prompt": state[self.input_key],
            "model": self.llm_model,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "seed": self.seed,
        }
        return {k: v for k, v in chat_kwargs.items() if v is not None}

    async def transform(self, state: VanillaState, **kwargs) -> VanillaState:
        resp = await self.shared.llm.chat(**self._prepare_chat_kwargs(state))
        state[self.output_key] = resp.generated_text
        cost = state.get(self.cost_key, LLMCost())
        i_tokens = resp.details.prompt_tokens or 0
        o_tokens = resp.details.generated_tokens or 0
        cost.input_tokens += i_tokens
        cost.output_tokens += o_tokens
        cost.total_tokens += i_tokens + o_tokens
        state[self.cost_key] = cost
        return state

    async def stream_transform(self, state: VanillaState, **kwargs):
        state[self.output_key] = ""
        async for token in self.shared.llm.stream_chat(**self._prepare_chat_kwargs(state)):
            state[self.output_key] += token.token.text
            if token.details.prompt_tokens or token.details.generated_tokens:
                cost = state.get(self.cost_key, LLMCost())
                i_tokens = token.details.prompt_tokens or 0
                o_tokens = token.details.generated_tokens or 0
                cost.input_tokens += i_tokens
                cost.output_tokens += o_tokens
                cost.total_tokens += i_tokens + o_tokens
                state[self.cost_key] = cost
            yield state


class Retriever(VanillaTransform):
    def __init__(
        self,
        retriever: BaseRetriever,
        input_key: list[str] = ["query", "doc_ids"],
        output_key: str = "chunks",
    ):
        super().__init__(input_key=input_key, output_key=output_key)
        self.retriever = retriever

    async def transform(self, state: VanillaState, **kwargs) -> VanillaState:
        state[self.output_key] = await self.retriever.retrieve(**self._get_input(state))
        return state


class Reranker(VanillaTransform):
    def __init__(
        self,
        reranker: BaseReranker,
        input_key: list[str] = ["query", "chunks"],
        output_key: str = "chunks",
    ):
        super().__init__(input_key=input_key, output_key=output_key)
        self.reranker = reranker

    async def transform(self, state: VanillaState, **kwargs) -> VanillaState:
        state[self.output_key] = await self.reranker.rerank(**self._get_input(state))
        return state
