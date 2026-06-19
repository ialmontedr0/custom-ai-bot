from collections.abc import Awaitable, Callable
from typing import cast

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types import User as TelegramUser

from src.db.models.user import User
from src.db.session import async_session_factory


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, object]], Awaitable[object]],
        event: TelegramObject,
        data: dict[str, object],
    ) -> object:
        telegram_user = cast(TelegramUser | None, data.get("event_from_user"))
        if telegram_user and not telegram_user.is_bot:
            async with async_session_factory() as session:
                from sqlalchemy import select

                result = await session.execute(
                    select(User).where(User.telegram_id == telegram_user.id)
                )
                user = result.scalar_one_or_none()
                if user is None:
                    user = User(
                        telegram_id=telegram_user.id,
                        username=telegram_user.username,
                        first_name=telegram_user.first_name,
                        language=telegram_user.language_code or "es",
                    )
                    session.add(user)
                    await session.commit()
                    await session.refresh(user)
                data["user"] = user
        return await handler(event, data)
