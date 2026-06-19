import structlog
from aiogram import Router
from aiogram.types import Message

from src.ai import AIService
from src.db.models.chat import Chat
from src.db.models.user import User
from src.db.session import async_session_factory

router = Router()
ai_service = AIService()
logger = structlog.get_logger()


@router.message()
async def handle_message(
    message: Message,
    user: User | None = None,
    chat: Chat | None = None,
) -> None:
    if not message.text or message.text.startswith("/"):
        return

    if user is None or chat is None:
        await message.answer("Error interno: no se pudo identificar el usuario o chat.")
        return

    async with async_session_factory() as session:
        try:
            response = await ai_service.process_message(
                session=session,
                user_id=user.id,
                chat_id=chat.id,
                text=message.text,
            )
        except Exception as e:
            logger.error("AI processing error", error=str(e), exc_info=True)
            await message.answer("ocurrio un error al procesar tu mensaje.")
            return

    if not response or not response.strip():
        await message.answer("El modelo no genero una respuesta.")
        return

    await message.answer(response)
