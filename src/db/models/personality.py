from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, UpdateableMixin, UUIDMixin


class Personality(UUIDMixin, UpdateableMixin, Base):
    __tablename__ = "personalities"

    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, default=0.7, nullable=False)
    max_tokens: Mapped[int] = mapped_column(Integer, default=2048, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    chats = relationship("Chat", back_populates="personality", lazy="selectin")
