from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from src.api.health import router as health_router
from src.api.webhook import router as webhook_router
from src.core.config import settings

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja startup y shutdown de la aplicacion.
    """
    logger.info("Inicio de la aplicacion.")
    # Aqui se inicializaran DB pool, redis, Qdrant, Aiogram, etc.
    yield
    # Aqui se cerraran conexiones
    logger.info("Cierre de la aplicacion")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Telegram AI Bot",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
    )

    # Rutas
    app.include_router(health_router)
    app.include_router(webhook_router)

    return app
