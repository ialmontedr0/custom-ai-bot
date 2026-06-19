from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.db.models.chat import Chat
from src.db.session import async_session_factory
from src.personality import PersonalityService

router = Router()
personality_service = PersonalityService()


@router.message(Command("modo"))
async def handle_personality(message: Message, chat: Chat | None = None) -> None:
    parts = message.text.split(maxsplit=1)
    name = parts[1].rstrip() if len(parts) > 1 else ""

    async with async_session_factory() as session:
        if not name:
            current_name = "Default"
            if chat and chat.personality_id:
                current = await personality_service.get_by_id(session, chat.personality_id)
                if current:
                    current_name = current.name

            all_personalities = await personality_service.get_all_active(session)

            if not all_personalities:
                await message.answer("No hay personalidades configuradas.")
                return

            lines = [f"Personalidad actual: {current_name}\n", "Disponibles:"]
            for p in all_personalities:
                marker = "  ACTUAL" if chat and chat.personality_id == p.id else ""
                lines.append(f"- {p.name}{marker}")
            lines.append("\nUsa: /modo [nombre]")
            await message.answer("\n".join(lines))
            return

        personality = await personality_service.get_by_name(session, name)

        if personality is None:
            await message.answer(f"No existe la personalidad '{name}'.")
            return

        if chat:
            await personality_service.assign_to_chat(session, chat.id, personality.id)
            await message.answer(f"Personalidad cambiada a: {personality.name}")
        else:
            await message.answer("Error: no se pudo identificar el chat")
