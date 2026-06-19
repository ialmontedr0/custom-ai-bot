from dataclasses import dataclass


@dataclass
class ChatMessage:
    role: str  # system | user | assistant
    content: str


@dataclass
class ChatRequest:
    messages: list[ChatMessage]
    model: str = ""
    temperature: float = 0.7
    max_tokens: int = 2048


@dataclass
class ChatResponse:
    content: str
    model: str
    tokens_prompt: int = 0
    tokens_completion: int = 0
    total_duration_ms: float = 0.0
