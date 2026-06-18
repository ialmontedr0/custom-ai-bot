import asyncio

from src.db.models import Personality
from src.db.session import async_session_factory, init_db


async def seed() -> None:
    await init_db()

    async with async_session_factory() as session:
        # Personalidad por defecto
        default = Personality(
            name="default",
            system_prompt=(
                "Eres un asistente tecnico experto en programacion."
                "Respondes de forma clara, directa y no tan tecnica."
                "Usas el idioma del usuario."
            ),
            temperature=0.7,
            max_tokens=2048,
            is_active=True,
        )
        session.add(default)
        print("Seed completado: personalidad 'default' creada")


if __name__ == "__main__":
    asyncio.run(seed())
