from telebot.types import Message
from utils.get_cache_file import get_cache_file
from utils.movie_utils import send_movie_info, random_movie, write_movie_of_day_data
from loader import bot
from config_data.config import MOVIE_OF_DAY_CACHE, BASE_PARAMS
from utils.decorators import ensure_user_registered, send_typing_action


@bot.message_handler(commands=["day"])
@ensure_user_registered
@send_typing_action
def day_handler(message: Message) -> None:
    """Обработчик команды |day"""

    # Получаем словарь с данными фильма дня
    movie: dict | None = get_cache_file(MOVIE_OF_DAY_CACHE, 1, random_movie, write_movie_of_day_data,
                                        {**BASE_PARAMS, "vote_count.gte": 1000, "vote_average.gte": 8.0,
                                         "primary_release_date.gte": "1990-01-01", "page": 1}, 1)
    if movie is None:
        bot.send_message(message.chat.id, "Не удалось получить фильм дня.")
        return

    # Выводим информацию о фильме пользователю в чат
    send_movie_info(bot, message.chat.id, message.from_user.id, [movie])
