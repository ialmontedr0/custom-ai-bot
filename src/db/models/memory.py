from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, TimestampMixin, UUIDMixin


class Memory(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "memories"

    user_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("users.id"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding_id: Mapped[str | None] = mapped_column(String(128), nullable=True, unique=True)
    importance: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)

    user = relationship("User", back_populates="memories", lazy="selectin")
