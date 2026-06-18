from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    return {"status": "OK", "service": "telegram-ai-bot"}


@router.get("/ready")
async def ready():
    # En el fututro: verificar DB, Redis, Qdrant
    return {"status": "ready"}
