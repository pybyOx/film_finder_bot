from telebot import TeleBot
from keyboards.inline.combined_keyboard import get_combined_keyboard
from telebot.types import InputMediaPhoto
from telebot.apihelper import ApiTelegramException
from models.movie_model import Movie
from utils.is_valid_image_url import is_valid_image_url


def send_movie_info(bot: TeleBot, chat_id: int, user_id: int, movie: Movie,  index: int, total: int,
                    message_id: int = None):
    """
    Составляет клавиатуру и текст сообщения.
    Отправляет информацию о фильме, либо редактируя сообщение (if message_id), либо отправляя новое (else).
    """

    keyboard = get_combined_keyboard(user_id, movie.movie_id, total, index)

    text = f"<b>{movie.title}</b> ({movie.year})\n" \
           f"🎭 Жанры: {movie.genres}\n" \
           f"⭐ Рейтинг: {movie.rating}\n\n" \
           f"{movie.overview}"

    if len(text) > 1024:
        text = text[1021] + '...'

    if message_id:
        try:
            if movie.poster_url and is_valid_image_url(movie.poster_url):
                media = InputMediaPhoto(media=movie.poster_url, caption=text, parse_mode="HTML")
                bot.edit_message_media(media, chat_id, message_id, reply_markup=keyboard)
            else:
                bot.edit_message_caption(text, chat_id, message_id, parse_mode="HTML", reply_markup=keyboard)
        except ApiTelegramException as e:
            if "message is not modified" not in str(e):
                raise
    else:
        if movie.poster_url and is_valid_image_url(movie.poster_url):
            bot.send_photo(chat_id, movie.poster_url, text, "HTML", reply_markup=keyboard)
        else:
            bot.send_message(chat_id, text, "HTML", reply_markup=keyboard)
