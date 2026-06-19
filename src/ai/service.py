import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.schemas import ChatMessage, ChatRequest
from src.ai.transformers_provider import TransformersProvider
from src.core.config import settings
from src.db.models.chat import Chat
from src.db.models.conversation import Conversation
from src.db.models.message import Message
from src.db.models.personality import Personality

logger = structlog.get_logger()
_provider: TransformersProvider | None = None


def get_provider() -> TransformersProvider:
    global _provider
    if _provider is None:
        _provider = TransformersProvider()
    return _provider


class AIService:
    async def process_message(
        self, session: AsyncSession, user_id: str, chat_id: str, text: str
    ) -> str:
        chat = await self._get_chat(session, chat_id)
        personality = await self._get_personality(session, chat.personality_id)
        conversation = await self._get_or_create_conversation(session, chat_id)

        await self._save_message(session, chat_id, user_id, "user", text)

        history = await self._get_history(session, chat_id, conversation.id)
        messages = self._build_messages(personality, history, text)

        request = ChatRequest(
            messages=messages,
            temperature=personality.temperature if personality else 0.7,
            max_tokens=personality.max_tokens if personality else 2048,
        )

        provider = get_provider()

        response = await provider.chat(request)

        await self._save_message(session, chat_id, user_id, "assistant", response.content)

        return response.content

    async def _get_chat(self, session: AsyncSession, chat_id: str) -> Chat:
        result = await session.execute(select(Chat).where(Chat.id == chat_id))
        chat = result.scalar_one_or_none()
        if chat is None:
            raise ValueError(f"Chat {chat_id} no encontrado")
        return chat

    async def _get_personality(
        self, session: AsyncSession, personality_id: str | None
    ) -> Personality | None:
        if personality_id is None:
            return None
        result = await session.execute(select(Personality).where(Personality.id == personality_id))
        return result.scalar_one_or_none()

    async def _get_or_create_conversation(
        self, session: AsyncSession, chat_id: str
    ) -> Conversation:
        result = await session.execute(
            select(Conversation)
            .where(Conversation.chat_id == chat_id)
            .order_by(Conversation.created_at.desc())
            .limit(1)
        )
        conversation = result.scalar_one_or_none()
        if conversation is None:
            conversation = Conversation(chat_id=chat_id)
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
        return conversation

    async def _save_message(
        self, session: AsyncSession, chat_id: str, user_id: str, role: str, content: str
    ) -> Message:
        msg = Message(chat_id=chat_id, user_id=user_id, role=role, content=content)
        session.add(msg)
        await session.commit()
        return msg

    async def _get_history(
        self, session: AsyncSession, chat_id: str, conversation_id: str
    ) -> list[Message]:
        result = await session.execute(
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at.desc())
            .limit(settings.memory_window_size)
        )
        return list(reversed(result.scalars().all()))

    def _build_messages(
        self, personality: Personality | None, history: list[Message], current_text: str
    ) -> list[ChatMessage]:
        messages: list[ChatMessage] = []

        if personality and personality.system_prompt:
            messages.append(ChatMessage(role="system", content=personality.system_prompt))

        for msg in history:
            messages.append(ChatMessage(role=msg.role, content=msg.content))

        messages.append(ChatMessage(role="user", content=current_text))

        return messages
