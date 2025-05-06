from telebot.types import Message
from loader import bot
from utils.cache_utils import get_cache_file
from utils.check_name import check_name
from utils.movie_utils import send_movie_info, random_movie, get_movie_details_by_id
from config_data.config import GENRES_CACHE_FILE, BASE_PARAMS
from api.tmdb_api import make_api_request
from utils.write_genres_data import write_genres_data
from utils.decorators import registration_check, send_typing_action
from keyboards.inline.pagination_state import user_pages, init_user_pages
from utils.exceptions import MovieNotFoundError

@bot.message_handler(commands=["genre"])
@registration_check
@send_typing_action
def genre_handler(message: Message) -> None:
    """Обработчик команды |genre"""

    # Проверка ввел ли пользователь название жанра
    genre_name = check_name(message, '/genre комедия')
    if genre_name is None:
        return

    # Поиск id введенного жанра из кэша жанров
    genres = get_cache_file(GENRES_CACHE_FILE, 7, make_api_request, write_genres_data,
                            "/genre/movie/list", BASE_PARAMS)
    genre_id = genres.get(genre_name.lower())
    if genre_id is None:
        bot.reply_to(message, f"Жанр '{genre_name}' не найден. Убедитесь, что вы ввели его корректно.")
        return

    # Получение списка фильмов по заданным параметрам
    params = {**BASE_PARAMS,
              "vote_count.gte": 1000,
              "vote_average.gte": 7.0,
              "primary_release_date.gte": "1990-01-01",
              "with_genres": str(genre_id),
              "page": 1}
    try:
        movies: list[dict] | None = random_movie(params, count=5)
        if not movies:
            raise MovieNotFoundError("Не удалось найти фильмы в жанре")

        movies = [get_movie_details_by_id(movie.get('id')) for movie in movies if movie]
        if not movies:
            raise MovieNotFoundError("Не удалось получить информацию о фильмах в жанре")

        init_user_pages(message.from_user.id, movies)

        send_movie_info(bot, message.chat.id, message.from_user.id, movies[0], len(movies))

    except MovieNotFoundError as error:
        bot.send_message(message.chat.id, f"{error} {genre_name}.")
        init_user_pages(message.from_user.id, [])
        return
