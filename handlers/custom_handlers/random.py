from telebot.types import Message
from utils.movie_utils import send_movie_info, random_movie, get_movie_details_by_id
from loader import bot
from config_data.config import BASE_PARAMS
from utils.decorators import ensure_user_registered, send_typing_action
from utils.exceptions import MovieNotFoundError


@bot.message_handler(commands=["random"])
@ensure_user_registered
@send_typing_action
def random_handler(message: Message) -> None:
    """Обработчик команды |random"""

    user_id = message.from_user.id
    try:
        # Получаем список с данными фильмов
        movies: list[dict] | None = random_movie({**BASE_PARAMS,
                                                  "vote_count.gte": 5000,
                                                  "vote_average.gte": 7.2,
                                                  "primary_release_date.gte": "1990-01-01",
                                                  "page": 1}, 10)
        if not movies:
            raise MovieNotFoundError("Не удалось получить случайный фильм.")

        movies_details: list[dict] = [get_movie_details_by_id(movie.get("id")) for movie in movies]
        if not movies_details:
            raise MovieNotFoundError("Ошибка запроса при попытке получить информацию о фильме.")

        send_movie_info(bot, message.chat.id, user_id, movies=movies_details)

    except MovieNotFoundError as error:
        bot.send_message(message.chat.id, error)
        return
