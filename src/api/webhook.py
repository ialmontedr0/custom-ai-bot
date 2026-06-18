import hmac

import structlog
from fastapi import APIRouter, Request

from src.core.config import settings

logger = structlog.get_logger()
router = APIRouter(tags=["webhook"])


def verify_webhook(secret: str, payload: bytes, signature: str) -> bool:
    """
    Verifica que el webhook venga de telegram
    """
    expected = hmac.new(secret.encode(), payload, "sha256").hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


@router.post("/webhook")
async def webhook(request: Request):
    """Recibe updates de telegram
    Args:
        request (Request)
    """
    # Verifica firma (produccion)
    # signature = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    # body = await request.body()
    # if not verify_webhook(settings.telegram_webhook_secret, body, signature):
    # return { "ok": False, "error": "invalid signature" }

    update_data = await request.json()
    logger.info("Webhook received", update_id=update_data.get("update_id"))

    # TODO: Pasar a Aiogram Dispatcher (Fase 4)

    return {"ok": True}
