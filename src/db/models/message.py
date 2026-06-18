from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, TimestampMixin, UUIDMixin


class Message(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "messages"

    chat_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("chats.id"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("users.id"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)

    chat = relationship("Chat", back_populates="messages", lazy="selectin")
    user = relationship("User", back_populates="messages", lazy="selectin")
