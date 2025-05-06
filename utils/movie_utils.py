from telebot import TeleBot
from random import randint, sample
from config_data.config import BASE_PARAMS, IMG_BASE_URL
from typing import Optional
from api.tmdb_api import make_api_request
from utils.format_datetime_ru import format_datetime_ru
from keyboards.inline.combined_keyboard import get_combined_keyboard
from keyboards.inline.pagination_state import user_pages


def send_movie_info(bot: TeleBot, chat_id: int, user_id: int, movie: dict, total: int):
    """Отправляет информацию о фильме с клавиатурой для пагинации и действий (в избранное, просмотрено)."""

    data: dict = user_pages[user_id]
    index: int = data["current_index"]
    is_favorites: bool = data["is_favorites"]

    # Генерируем клавиатуру с пагинацией и кнопками
    keyboard = get_combined_keyboard(user_id, movie, total, index, is_favorites)

    genres_str = ", ".join(movie.get("genres", [])) or "Жанры не указаны"
    datetime_str = f"_Дата поиска: {format_datetime_ru(movie['datetime'])}_\n" if "datetime" in movie else ""

    text = f"*{movie['title']}* ({movie['release_date']})\n" \
           f"🎭 Жанры: {genres_str}\n" \
           f"⭐ Рейтинг: {movie['rating']}\n\n" \
           f"{movie['overview'] or 'Нет описания'}\n\n" \
           f"{datetime_str}"

    if movie.get("poster_url"):
        bot.send_photo(chat_id=chat_id,
                       photo=movie["poster_url"],
                       caption=text,
                       parse_mode="Markdown",
                       reply_markup=keyboard)
    else:
        bot.send_message(chat_id=chat_id,
                         text=text,
                         parse_mode="Markdown",
                         reply_markup=keyboard)


def get_movie_details_by_id(id_movie: int) -> Optional[dict]:
    """Запрос информации о фильме по его id"""

    # Получаем всю информацию о фильме
    data: dict = make_api_request(f"/movie/{id_movie}", BASE_PARAMS)
    if not data:  # Если словарь пуст значит возникла ошибка запроса
        return None

    # Возвращаем словарь с нужными данными
    return {"movie_id": id_movie,
            "title": data.get("title"),
            "overview": data.get("overview"),
            "release_date": data.get("release_date", "")[:4],
            "rating": data.get("vote_average"),
            "poster_url": IMG_BASE_URL + data["poster_path"] if data.get("poster_path") else None,
            "genres": [genre["name"] for genre in data.get("genres", [])]}


def random_movie(params: dict, count: int) -> Optional[list]:

    # Получаем все фильмы по заданным фильтрам
    all_movies = make_api_request('/discover/movie', params)
    if not all_movies:
        return None

    # Рандомно выбираем одну страницу
    random_page = randint(1, all_movies.get("total_pages"))
    params["page"] = random_page

    # Получаем с этой страницы все фильмы
    movies_from_page = make_api_request('/discover/movie', params)
    if not movies_from_page:
        return None
    movie_list = movies_from_page.get("results", [])
    if not movie_list:
        return None

    # Рандомно выбираем из них заданное количество уникальных фильмов
    movies = sample(movie_list, min(count, len(movie_list)))
    return movies


def write_movie_of_day_data(movie_of_day: list) -> dict:
    """Функция для записи фильма дня"""
    return get_movie_details_by_id(movie_of_day[0].get("id"))
