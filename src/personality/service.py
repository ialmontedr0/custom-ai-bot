import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.chat import Chat
from src.db.models.personality import Personality

logger = structlog.get_logger()


class PersonalityService:
    async def get_all_active(self, session: AsyncSession) -> list[Personality]:
        result = await session.execute(
            select(Personality).where(Personality.is_active).order_by(Personality.name)
        )
        return list(result.scalars().all())

    async def get_by_name(self, session: AsyncSession, name: str) -> Personality | None:
        result = await session.execute(select(Personality).where(Personality.name.ilike(name)))
        return result.scalar_one_or_none()

    async def get_by_id(self, session: AsyncSession, personality_id: str) -> Personality | None:
        result = await session.execute(select(Personality).where(Personality.id == personality_id))
        return result.scalar_one_or_none()

    async def assign_to_chat(
        self, session: AsyncSession, chat_id: str, personality_id: str | None
    ) -> Chat:
        result = await session.execute(select(Chat).where(Chat.id == chat_id))
        chat = result.scalar_one_or_none()
        if chat is None:
            raise ValueError(f"Chat {chat_id} no encontrado")
        chat.personality_id = personality_id
        await session.commit()
        await session.refresh(chat)
        return chat
