from abc import ABC, abstractmethod

from src.ai.schemas import ChatRequest, ChatResponse


class LLMProvider(ABC):
    @abstractmethod
    async def chat(self, request: ChatRequest) -> ChatResponse: ...
