from collections.abc import Awaitable, Callable
from typing import cast

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from src.cache.rate_limiter import RateLimiter


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, rate_limiter: RateLimiter) -> None:
        self.rate_limiter = rate_limiter

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, object]], Awaitable[object]],
        event: TelegramObject,
        data: dict[str, object],
    ) -> object:
        user = cast(User | None, data.get("event_from_user"))
        if user:
            allowed = await self.rate_limiter.check(str(user.id))
            if not allowed:
                from aiogram.types import Message

                if isinstance(event, Message):
                    await event.answer(" Demasiadas solicitudes. Espera un momento.")
                return None
        return await handler(event, data)
