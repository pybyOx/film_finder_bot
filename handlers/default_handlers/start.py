from telebot.types import Message
from loader import bot
from utils.decorators import ensure_user_registered, send_typing_action


@bot.message_handler(commands=["start"])
@ensure_user_registered
@send_typing_action
def day_handler(message: Message) -> None:
    """Обработчик команды |start"""
