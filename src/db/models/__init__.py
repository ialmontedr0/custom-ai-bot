from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        server_default=func.now(),
        nullable=False,
    )


class UpdateableMixin(TimestampMixin):
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, onupdate=lambda: datetime.now(UTC), nullable=True
    )


class UUIDMixin:
    id: Mapped[str] = mapped_column(
        String(32),
        primary_key=True,
        default=lambda: uuid4().hex,
    )


from src.db.models.user import User
from src.db.models.chat import Chat
from src.db.models.message import Message
from src.db.models.conversation import Conversation
from src.db.models.personality import Personality
from src.db.models.memory import Memory
from src.db.models.document import Document

__all__ = [
    "Base",
    "TimestampMixin",
    "UpdateableMixin",
    "UUIDMixin",
    "User",
    "Chat",
    "Message",
    "Conversation",
    "Personality",
    "Memory",
    "Document",
]
