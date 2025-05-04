from telebot.types import Message
from loader import bot
from utils.check_name import check_name
from utils.movie_utils import send_movie_info, get_movie_details_by_id
from utils.decorators import registration_check, send_typing_action
from api.tmdb_api import make_api_request
from config_data.config import BASE_PARAMS
from utils.exceptions import MovieNotFoundError
from utils.save_movie_to_history import save_movie_to_history
from keyboards.inline.pagination_state import user_pages
from keyboards.inline.pagination_utils import show_movie_page
import re


@bot.message_handler(commands=["movie"])
@registration_check
@send_typing_action
def movie_handler(message: Message) -> None:
    """Обработчик команды |movie"""

    # Проверка ввел ли пользователь название фильма
    user_title: str | None = check_name(message, '/movie Интерстеллар')
    if not user_title:
        return
    user_title = user_title.lower()

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

            movie_title = movie["title"].lower()

            # Убедимся что user_title не является подстрокой movie_title
            if not re.search(rf'\b{re.escape(user_title)}\b', movie_title):
                continue

            # по id фильма запрашиваем доп информацию и записываем в словарь
            movie_details: dict | None = get_movie_details_by_id(movie.get('id'))
            if not movie_details:
                continue

            # Если найдено точное совпадение по названию
            if movie_title == user_title:

                # Сохраняем данные фильма в историю поиска пользователя
                save_movie_to_history(message.from_user.id, movie_details)

                # Выводим пользователю в чат
                send_movie_info(bot, message.chat.id, movie_details)
                return

            # Заносим данные в список для показа через пагинацию (на случай если точного совпадения не найдется)
            else:
                movies.append(movie_details)

        if not movies:
            raise MovieNotFoundError("Не удалось получить данные ни по одному фильму.")

        # Если точного совпадения не найдено выводим все результаты поиска

        # Записываем данные в хранилище состояния пользователя
        user_pages[message.from_user.id] = {'movies': movies, "current_index": 0}

        # Выводим результаты с помощью пагинации
        show_movie_page(message.chat.id, message.from_user.id)

    except MovieNotFoundError as error:
        bot.send_message(message.chat.id, error)
