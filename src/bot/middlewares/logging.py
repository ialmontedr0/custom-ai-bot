from collections.abc import Awaitable, Callable
from typing import cast

import structlog
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update, User

logger = structlog.get_logger()


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, object]], Awaitable[object]],
        event: TelegramObject,
        data: dict[str, object],
    ) -> object:
        update = cast(Update | None, data.get("event_update"))
        user = cast(User | None, data.get("event_from_user"))
        if update:
            logger.info(
                "Update received",
                update_id=update.update_id,
                user_id=user.id if user else None,
                username=user.username if user else None,
            )
        return await handler(event, data)
