from aiogram.filters import BaseFilter
from aiogram.types import Message

COMMANDS = {"/start", "/help", "/resumen", "/buscar", "/aprende", "/modo", "/personalidad"}


class CommandFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        command = message.text.split()[0].lower()
        return command in COMMANDS
