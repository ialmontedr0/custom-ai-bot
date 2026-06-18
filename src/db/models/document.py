from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, TimestampMixin, UUIDMixin


class Document(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "documents"

    chat_id: Mapped[str | None] = mapped_column(
        String(32), ForeignKey("chats.id"), nullable=True
    )
    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    file_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False)

    chat = relationship("Chat", back_populates="documents", lazy="selectin")
    user = relationship("User", back_populates="documents", lazy="selectin")
