from telebot.types import Message
from utils.cache_utils import get_cache_file
from utils.movie_utils import send_movie_info, random_movie, write_movie_of_day_data
from loader import bot
from config_data.config import MOVIE_OF_DAY_CACHE, BASE_PARAMS
from utils.decorators import registration_check, send_typing_action
from keyboards.inline.pagination_state import user_pages, init_user_pages


@bot.message_handler(commands=["day"])
@registration_check
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

    user_id = message.from_user.id
    init_user_pages(user_id, [movie], 0)

    # Выводим информацию о фильме пользователю в чат
    send_movie_info(bot, message.chat.id, user_id, movie, 1)
