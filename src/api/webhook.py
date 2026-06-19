import structlog
from aiogram.types import Update
from fastapi import APIRouter, Request

from src.bot.dispatcher import bot, dp
from src.core.config import settings

logger = structlog.get_logger()
router = APIRouter(tags=["webhook"])


async def set_webhook() -> None:
    if settings.telegram_webhook_url:
        await bot.set_webhook(
            url=f"{settings.telegram_webhook_url}/webhook",
            secret_token=settings.telegram_webhook_secret,
            drop_pending_updates=True,
        )
        logger.info("Webhook set", url=settings.telegram_webhook_url)


async def delete_webhook() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook deleted")


@router.post("/webhook")
async def webhook(request: Request) -> dict[str, bool | str]:
    token = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")

    if token != settings.telegram_webhook_secret:
        logger.warning("Invalid webhook secret token")
        return {"ok": False, "error": "invalid secret token"}

    body = await request.json()
    update = Update.model_validate(body)
    await dp.feed_update(bot=bot, update=update)
    return {"ok": True}
