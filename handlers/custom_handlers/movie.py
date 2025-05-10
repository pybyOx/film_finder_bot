from telebot.types import Message
from loader import bot
from utils.check_name import check_name
from utils.movie_utils import send_movie_info, get_movie_details_by_id
from utils.decorators import ensure_user_registered, send_typing_action
from api.tmdb_api import make_api_request
from config_data.config import BASE_PARAMS
from utils.exceptions import MovieNotFoundError
import re
from keyboards.inline.pagination_state import init_user_pages


@bot.message_handler(commands=["movie"])
@ensure_user_registered
@send_typing_action
def movie_handler(message: Message) -> None:
    """Обработчик команды |movie"""

    # Проверка ввел ли пользователь название фильма
    user_title: str | None = check_name(message, '/movie Интерстеллар')
    if not user_title:
        return

    user_title = user_title.lower()
    user_id = message.from_user.id

    try:
        # Получаем словарь с результатами запроса к api
        data: dict = make_api_request('/search/movie', params={**BASE_PARAMS,
                                                               "query": user_title,
                                                               "include_adult": False})

        results: list[dict] | None = data.get("results")
        if not results:  # если словарь data пуст, не содержит ключа 'results' или data['results'] == []
            raise MovieNotFoundError("Фильм не найден. Попробуйте другое название.")

        movies = []

        for movie in results:

            # Убедимся что user_title не является подстрокой movie_title
            movie_title = movie["title"].lower()
            if not re.search(rf'\b{re.escape(user_title)}\b', movie_title):
                continue

            # Получаем детали фильма по его id
            movie_details = get_movie_details_by_id(movie.get('id'))
            if not movie_details:
                raise MovieNotFoundError("Возникла ошибка запроса при попытке получения информации о фильме")

            # Если найдено точное совпадение по названию
            if movie_title == user_title:

                send_movie_info(bot, message.chat.id, user_id, [movie_details])
                return

            # Заносим данные в список для показа через пагинацию (на случай если точного совпадения не найдется)
            movies.append(movie_details)

        if not movies:
            raise MovieNotFoundError("Не удалось получить данные ни по одному фильму.")

        # Если точного совпадения не найдено выводим все результаты поиска
        send_movie_info(bot, message.chat.id, user_id, movies)

    except MovieNotFoundError as error:
        bot.send_message(message.chat.id, error)
