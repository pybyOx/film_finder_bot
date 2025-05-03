from telebot.types import Message
from loader import bot
from utils.check_name import check_name
from utils.movie_utils import send_movie_info, get_movie_details_by_id
from utils.decorators import registration_check, send_typing_action
from api.tmdb_api import make_api_request
from config_data.config import BASE_PARAMS
from utils.exceptions import MovieNotFoundError
from utils.save_movie_to_history import save_movie_to_history


@bot.message_handler(commands=["movie"])
@registration_check
@send_typing_action
def movie_handler(message: Message) -> None:
    """Обработчик команды |movie"""

    # Проверка ввел ли пользователь название фильма
    movie_title = check_name(message, '/movie Интерстеллар')
    if movie_title is None:
        return

    try:
        # Получаем словарь с результатами запроса к api
        data: dict = make_api_request('/search/movie', params={**BASE_PARAMS,
                                                               "query": movie_title,
                                                               "include_adult": False})

        results: list[dict] | None = data.get("results")
        if not results:  # если словарь data пуст, не содержит ключа 'results' или data['results'] == []
            raise MovieNotFoundError("Фильм не найден. Попробуйте другое название.")

        # Ищем точное совпадение по названию
        for movie in results:
            # Если точное совпадение найдено
            if movie["title"].lower() == movie_title.lower():

                # по id фильма запрашиваем доп информацию и записываем в словарь
                movie_details: dict | None = get_movie_details_by_id(movie.get('id'))
                if not movie_details:
                    raise MovieNotFoundError("Произошла ошибка запроса информации о фильме")

                # Сохраняем данные фильма в историю поиска пользователя
                save_movie_to_history(message.from_user.id, movie_details)

                # Выводим пользователю в чат
                send_movie_info(bot, message.chat.id, movie_details)
                return

    except MovieNotFoundError as error:
        bot.send_message(message.chat.id, error)
