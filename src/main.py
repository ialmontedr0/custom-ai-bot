import structlog

from src.api.app import create_app
from src.core.config import settings

logger = structlog.get_logger()


def main():
    app = create_app()
    logger.info(
        "Iniciando aplicacion",
        environment=settings.environment,
        log_level=settings.log_level,
    )
    return app


app = main()
