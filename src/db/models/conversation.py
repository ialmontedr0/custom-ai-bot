from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, TimestampMixin, UUIDMixin


class Conversation(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "conversations"

    chat_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("chats.id"), nullable=False, index=True
    )
    title: Mapped[str | None] = mapped_column(String(512), nullable=True)

    chat = relationship("Chat", back_populates="conversations", lazy="selectin")
