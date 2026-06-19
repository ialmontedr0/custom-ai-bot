from aiogram import Router
from aiogram.types import Message
from aiogram.types import User as TelegramUser

from src.db.models.chat import Chat
from src.db.models.user import User

router = Router()


@router.message()
async def handle_message(
    message: Message,
    user: User | None = None,
    chat: Chat | None = None,
) -> None:
    if not message.text:
        return
    if message.text.startswith("/"):
        return

    telegram_user: TelegramUser | None = message.from_user
    user_display = telegram_user.first_name if telegram_user else "Usuario"

    response = (
        f"Hola {user_display}! Tu mensaje fue recibido.\n\n"
        f"Has dicho: _{message.text}_\n\n"
        "El motor de IA aun no esta conectado."
    )

    await message.answer(response)
