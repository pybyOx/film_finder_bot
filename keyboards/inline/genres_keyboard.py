from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.get_cache_file import get_genres


async def get_genre_keyboard() -> InlineKeyboardMarkup:
    """
    :raise ResponseError: Ошибка запроса к api
    :return: Клавиатура с названиями жанров
    """
    genres = await get_genres()
    keyboard = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(text=genre_name.title(), callback_data=f"genre:{genre_name}")
               for genre_name in genres if genre_name != "телевизионный фильм"]

    # Добавляем кнопки по 4 в ряд
    for i in range(0, len(buttons), 3):
        keyboard.row(*buttons[i:i + 3])

    return keyboard
