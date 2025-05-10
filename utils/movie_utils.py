from telebot import TeleBot
from telebot.types import InputMediaPhoto, InputMedia
from random import randint, sample
from config_data.config import BASE_PARAMS, IMG_BASE_URL
from typing import Optional
from api.tmdb_api import make_api_request
from keyboards.inline.combined_keyboard import get_combined_keyboard
from keyboards.inline.pagination_state import get_data_from_user_pages, init_user_pages


def send_movie_info(bot: TeleBot, chat_id: int, user_id: int,
                    movies: list[dict] = None, is_favorite: bool = False, message_id: int = None):
    """
    Обновляет данные user_pages (if movies); и получает из него данные.
    С учетом этих данных составляет клавиатуру и текст сообщения.
    Отправляет информацию о фильме, либо редактируя сообщение (if message_id), либо отправляя новое (else).
    """

    if movies:
        init_user_pages(user_id, movies, is_favorite=is_favorite)

    data, movies, index, movie, total, is_favorite = get_data_from_user_pages(user_id)
    keyboard = get_combined_keyboard(user_id, movie, total, index, is_favorite)

    text = f"*{movie['title']}* ({movie['year']})\n" \
           f"🎭 Жанры: {movie['genres']}\n" \
           f"⭐ Рейтинг: {movie['rating']}\n\n" \
           f"{movie['overview'] or 'Нет описания'}\n\n"

    if message_id and movie.get("poster_url"):

        bot.edit_message_media(media=InputMediaPhoto(media=movie["poster_url"], caption=text, parse_mode="Markdown"),
                               chat_id=chat_id, message_id=message_id, reply_markup=keyboard)

    elif message_id:

        bot.edit_message_caption(chat_id=chat_id, message_id=message_id,
                                 caption=text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        if movie.get("poster_url"):

            bot.send_photo(chat_id=chat_id, photo=movie["poster_url"],
                           caption=text, parse_mode="Markdown", reply_markup=keyboard)
        else:
            bot.send_message(chat_id=chat_id, text=text,
                             parse_mode="Markdown", reply_markup=keyboard)


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
            "year": data.get("release_date", "")[:4],
            "rating": data.get("vote_average"),
            "poster_url": IMG_BASE_URL + data["poster_path"] if data.get("poster_path") else None,
            "genres": ", ".join([genre["name"] for genre in data.get("genres", [])])}


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
