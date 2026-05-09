from loader import bot
from utils.get_cache_file import get_genres
from utils.random_movie import random_movie
from config_data.config import BASE_PARAMS
from utils.exceptions import MovieNotFoundError, ResponseError
from states.pagination_state import PageState, USER_PAGES
from telebot.types import CallbackQuery
from utils.send_movie_info import send_movie_info


@bot.callback_query_handler(func=lambda call: call.data.startswith("genre:"))
async def handle_genre_callback(call: CallbackQuery):
    """Обработчик кнопок с названиями жанров"""
    from models.movie_model import Movie
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    genre_name = call.data.split(":", 1)[1]

    try:
        genres = await get_genres()
        genre_id = genres.get(genre_name.lower())
        if not genre_id:
            raise ValueError(f"Жанр '{genre_name}' не найден. Убедитесь, что вы ввели его корректно.")

        # Получение 10 случайных фильмов по заданным параметрам
        params = {**BASE_PARAMS,
                  "vote_count.gte": 1000,
                  "vote_average.gte": 7.0,
                  "primary_release_date.gte": "1990-01-01",
                  "with_genres": str(genre_id),
                  "page": 1}

        results = await random_movie(params, count=10)
        movies = [Movie(movie, genres) for movie in results]

        state = PageState(movies)
        USER_PAGES.set_state(user_id, state)

        send_movie_info(bot, chat_id, user_id, movies[0], state.current_index, state.total())

    except (MovieNotFoundError, ResponseError, ValueError) as error:
        bot.answer_callback_query(call.id, text=str(error), show_alert=True)
