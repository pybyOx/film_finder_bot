from telebot.types import Message
from utils.random_movie import random_movie
from loader import bot
from config_data.config import BASE_PARAMS
from utils.decorators import ensure_user_registered, send_typing_action
from utils.exceptions import MovieNotFoundError, ResponseError
from models.movie_model import Movie
from states.pagination_state import PageState, USER_PAGES
from utils.send_movie_info import send_movie_info


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

        movie_objects = [Movie(movie) for movie in movies]
        if not movie_objects:
            raise MovieNotFoundError("Ошибка запроса при попытке получить информацию о фильме.")

        state = PageState(movie_objects)
        USER_PAGES.set_state(user_id, state)

        send_movie_info(bot, message.chat.id, user_id, movie_objects[0], state.current_index, state.total())

    except MovieNotFoundError as error:
        bot.send_message(message.chat.id, error)
    except ResponseError as error:
        bot.send_message(message.chat.id, error)
