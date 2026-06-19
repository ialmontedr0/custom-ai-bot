from collections.abc import Awaitable, Callable
from typing import cast

from aiogram import BaseMiddleware
from aiogram.types import Chat as TelegramChat
from aiogram.types import TelegramObject

from src.db.models.chat import Chat
from src.db.session import async_session_factory


class ContextMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, object]], Awaitable[object]],
        event: TelegramObject,
        data: dict[str, object],
    ) -> object:
        telegram_chat = cast(TelegramChat | None, data.get("event_chat"))
        if telegram_chat:
            async with async_session_factory() as session:
                from sqlalchemy import select

                result = await session.execute(
                    select(Chat).where(Chat.telegram_chat_id == telegram_chat.id)
                )
                chat_obj = result.scalar_one_or_none()
                if chat_obj is None:
                    chat_obj = Chat(
                        telegram_chat_id=telegram_chat.id,
                        chat_type=telegram_chat.type,
                        title=telegram_chat.title,
                    )
                    session.add(chat_obj)
                    await session.commit()
                    await session.refresh(chat_obj)
                data["chat"] = chat_obj
        return await handler(event, data)
