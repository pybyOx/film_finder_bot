from telebot.types import Message
from loader import bot
from utils.check_name import check_name
from utils.decorators import ensure_user_registered, send_typing_action
from api.tmdb_api import make_api_request
from config_data.config import BASE_PARAMS
from utils.exceptions import MovieNotFoundError, ResponseError, ArgumentError
import re
from models.movie_model import Movie
from states.pagination_state import PageState, USER_PAGES
from utils.send_movie_info import send_movie_info


@bot.message_handler(commands=["movie"])
@ensure_user_registered
@send_typing_action
def movie_handler(message: Message) -> None:
    """Обработчик команды |movie"""
    chat_id = message.chat.id
    user_id = message.from_user.id

    try:
        user_title = check_name(message, '/movie Интерстеллар').lower()

        # Получаем словарь с результатами запроса к api
        response: dict = make_api_request('/search/movie', params={**BASE_PARAMS,
                                                                   "query": user_title,
                                                                   "include_adult": False})

        results = response.get("results")
        if not results:
            raise MovieNotFoundError("Фильм не найден. Попробуйте другое название.")

        movies = []

        for movie in results:

            # Убедимся что user_title не является подстрокой movie_title
            movie_title = movie["title"].lower()
            if not re.search(rf'\b{re.escape(user_title)}\b', movie_title):
                continue

            movie = Movie(movie)

            # Если найдено точное совпадение по названию
            if movie_title == user_title:

                state = PageState([movie])
                USER_PAGES.set_state(user_id, state)

                send_movie_info(bot, chat_id, user_id, movie,
                                state.current_index, state.total())
                return

            # Заносим данные в список для показа через пагинацию (на случай если точного совпадения не найдется)
            movies.append(movie)

        if not movies:
            raise MovieNotFoundError("Не удалось получить данные ни по одному фильму.")

        # Если точного совпадения не найдено выводим все результаты поиска
        state = PageState(movies)
        USER_PAGES.set_state(user_id, state)

        send_movie_info(bot, chat_id, user_id, movies[0], state.current_index, state.total())

    except MovieNotFoundError as error:
        bot.send_message(message.chat.id, error)
    except ResponseError as error:
        bot.send_message(message.chat.id, error)
    except ArgumentError as error:
        bot.send_message(message.chat.id, error)
