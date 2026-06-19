from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def start(message: Message) -> None:
    await message.answer(
        "Hola.\n\n"
        "Que tal todo?\n"
        "Comandos:\n"
        "/resumen - Resumir conversacion\n"
        "/buscar [consulta] - Buscar en internet\n"
        "/aprende - Aprender un documento\n"
        "/modo - Cambiar personalidad"
    )


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        "Comandos:\n\n"
        "/start - Iniciar bot\n"
        "/help - Mostar ayuda\n"
        "/resumen - Resumir ultimos mensajes\n"
        "/buscar [consulta] - Buscar en internet"
        "/aprende - Subir documento para aprender\n"
        "/modo [nombre] - Cambiar personalidad"
    )
