from telebot.types import Message
from loader import bot
from utils.decorators import ensure_user_registered, send_typing_action
from keyboards.inline.genres_keyboard import get_genre_keyboard


@bot.message_handler(commands=["genre"])
@ensure_user_registered
@send_typing_action
def genre_handler(message: Message) -> None:
    """Показывает клавиатуру с жанрами"""
    bot.send_message(message.chat.id, "Выберите жанр:", reply_markup=get_genre_keyboard())
