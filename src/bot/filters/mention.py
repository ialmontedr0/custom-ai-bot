from aiogram.filters import BaseFilter
from aiogram.types import Message


class MentionFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        bot = message.bot
        if bot is None:
            return False
        bot_username = (await bot.me()).username
        if bot_username is None:
            return False
        # Detecta @botusername al inicio, medio, o reply al bot
        if f"@{bot_username}" in message.text:
            return True
        if message.reply_to_message and message.reply_to_message.from_user:
            return message.reply_to_message.from_user.id == bot.id
        return False
