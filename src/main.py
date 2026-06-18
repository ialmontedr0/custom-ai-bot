import structlog
from fastapi import FastAPI

from src.api.app import create_app
from src.core.config import settings

logger = structlog.get_logger()


def main() -> FastAPI:
    app = create_app()
    logger.info(
        "Starting application",
        environment=settings.environment,
        log_level=settings.log_level,
    )
    return app


app = main()
