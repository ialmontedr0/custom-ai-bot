from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.bot.handlers.commands import router as commands_router
from src.bot.handlers.messages import router as messages_router
from src.bot.handlers.personality import router as personality_router
from src.bot.middlewares.auth import AuthMiddleware
from src.bot.middlewares.context import ContextMiddleware
from src.bot.middlewares.logging import LoggingMiddleware
from src.core.config import settings

bot = Bot(
    token=settings.telegram_bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()


def setup_dispatcher() -> None:
    dp.update.middleware(LoggingMiddleware())
    dp.update.middleware(AuthMiddleware())
    dp.update.middleware(ContextMiddleware())

    dp.include_router(personality_router)
    dp.include_router(commands_router)
    dp.include_router(messages_router)
