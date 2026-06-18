from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, TimestampMixin, UUIDMixin


class Chat(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "chats"

    telegram_chat_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False
    )
    chat_type: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str | None] = mapped_column(String(512), nullable=True)
    personality_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("personalities.id"), nullable=True
    )

    messages = relationship("Message", back_populates="chat", lazy="selectin")
    conversations = relationship("Conversation", back_populates="chat", lazy="selectin")
    personality = relationship("Personality", back_populates="chats", lazy="selectin")
    documents = relationship("Document", back_populates="chat", lazy="selectin")
