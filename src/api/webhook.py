import hmac

import structlog
from fastapi import APIRouter, Request

logger = structlog.get_logger()
router = APIRouter(tags=["webhook"])


def verify_webhook(secret: str, payload: bytes, signature: str) -> bool:
    """
    Verifica que el webhook venga de telegram
    """
    expected = hmac.new(secret.encode(), payload, "sha256").hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


@router.post("/webhook")
async def webhook(request: Request) -> dict[str, bool | str]:
    update_data = await request.json()
    logger.info("Webhook received", update_id=update_data.get("update_id"))
    return {"ok": True}
