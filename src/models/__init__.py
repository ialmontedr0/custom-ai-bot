"""
Schemas Pydantic para la API y servicios.

Cada modelo tiene:
- CreateSchema: para crear (sin id, sin timestamps)
- UpdateSchema: para actualizar (todos opcionales)
- ResponseSchema: para devolver al cliente
"""

from src.models.document import DocumentCreate, DocumentResponse
from src.models.memory import MemoryCreate, MemoryResponse
from src.models.personality import PersonalityCreate, PersonalityResponse, PersonalityUpdate

from src.models.chat import ChatCreate, ChatResponse, ChatUpdate
from src.models.message import MessageCreate, MessageResponse
from src.models.user import UserCreate, UserResponse, UserUpdate

__all__ = [
    "UserCreate",
    "UserResponse",
    "UserUpdate",
    "ChatCreate",
    "ChatResponse",
    "ChatUpdate",
    "MessageCreate",
    "MessageResponse",
    "PersonalityCreate",
    "PersonalityResponse",
    "PersonalityUpdate",
    "DocumentCreate",
    "DocumentResponse",
    "MemoryCreate",
    "MemoryResponse",
]
