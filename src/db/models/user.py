from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, UpdateableMixin, UUIDMixin


class User(UUIDMixin, UpdateableMixin, Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(128), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="es", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    messages = relationship("Message", back_populates="user", lazy="selectin")
    memories = relationship("Memory", back_populates="user", lazy="selectin")
    documents = relationship("Document", back_populates="user", lazy="selectin")
