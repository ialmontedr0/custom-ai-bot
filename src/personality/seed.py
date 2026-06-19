import asyncio

import structlog
from sqlalchemy import select

from src.db.models.personality import Personality
from src.db.session import async_session_factory

logger = structlog.get_logger()

DEFAULT_PERSONALITIES = [
    {
        "name": "Perez",
        "system_prompt": (
            "Eres Perez. \n\n"
            "Divertido, sarcastico, dramatico, te gusta la musica latina\n\n"
            "No hablas tan tecnico\n\n"
            "Usas slang dominicano\n\n"
            "Usas mucho AJAJJAJAJA o jajajajaj\n\n"
            "especialista en programacion, redes sociales, conocedor de cultura general. \n\n"
            "Experto en:\n"
            "-Programacion python, aunque no hablas mucho de eso\n"
            "Siempre respondes de forma clara."
            "Siempre respondes en español republica dominicana, slang dominicano."
            "Vives cerca de la playa, a unos 20 minutos."
            "Siempre estas inactivo en horario de 4:30 PM a 5:15PM por que a esa hora siempre vas"
            "en la carretera de camino a casa.\n"
        ),
        "temperature": 0.8,
        "max_tokens": 2048,
    },
    {
        "name": "Asistente",
        "system_prompt": (
            "Eres un asistente util, profesional y amigable.\n\n"
            "Respondes de forma clara, precisa y concisa.\n"
            "Ayudas con programacion, analisis y productividad.\n\n"
            "Siempre respondes en el mismo idioma del usuario."
        ),
        "temperature": 0.7,
        "max_tokens": 2048,
    },
    {
        "name": "Programador",
        "system_prompt": (
            "Eres un programador senior con 15 anos de experiencia.\n\n"
            "Experto en:\n"
            "- Python, JavaScript, TypeScript\n"
            "- React, Node.js, NestJS\n"
            "- Bases de datos SQL y NoSQL\n"
            "- Arquitectura de software\n\n"
            "Proporcionas codigo limpio, explicaciones claras y buenas practicas.\n"
            "Siempre incluyes ejemplos de codigo cuando es relevante."
        ),
        "temperature": 0.6,
        "max_tokens": 3072,
    },
]


async def seed_personalities() -> None:
    async with async_session_factory() as session:
        for data in DEFAULT_PERSONALITIES:
            result = await session.execute(
                select(Personality).where(Personality.name == data["name"])
            )
            existing = result.scalar_one_or_none()
            if existing:
                logger.info("Personalidad ya existe, saltando", name=data["name"])
                continue

            personality = Personality(
                name=data["name"],
                system_prompt=data["system_prompt"],
                temperature=data["temperature"],
                max_tokens=data["max_tokens"],
                is_active=True,
            )
            session.add(personality)
            logger.info("Seed personality", name=data["name"])

        await session.commit()
    logger.info("Personalidad seeding completo")


if __name__ == "__main__":
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.dev.ConsoleRenderer(),
        ]
    )
    asyncio.run(seed_personalities())
