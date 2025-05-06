from telebot.types import Message
from utils.movie_utils import send_movie_info, random_movie, get_movie_details_by_id
from loader import bot
from config_data.config import BASE_PARAMS
from utils.decorators import registration_check, send_typing_action
from keyboards.inline.pagination_state import init_user_pages
from utils.exceptions import MovieNotFoundError


@bot.message_handler(commands=["random"])
@registration_check
@send_typing_action
def random_handler(message: Message) -> None:
    """Обработчик команды |random"""

    user_id = message.from_user.id
    try:
        # Получаем список с данными случайного фильма
        movie: list[dict] | None = random_movie({**BASE_PARAMS,
                                                 "vote_count.gte": 5000,
                                                 "vote_average.gte": 7.2,
                                                 "primary_release_date.gte": "1990-01-01",
                                                 "page": 1}, 1)
        if not movie:
            raise MovieNotFoundError("Не удалось получить случайный фильм.")

        movie: dict | None = get_movie_details_by_id(movie[0].get("id"))
        if not movie:
            raise MovieNotFoundError("Ошибка запроса при попытке получить информацию о фильме.")

        init_user_pages(user_id, [movie])

        send_movie_info(bot, message.chat.id, user_id, movie, 1)

    except MovieNotFoundError as error:
        bot.send_message(message.chat.id, error)
        init_user_pages(user_id, [])
        return
