from telebot import TeleBot
from random import randint, sample
from config_data.config import BASE_PARAMS, IMG_BASE_URL
from typing import Optional
from api.tmdb_api import make_api_request


def send_movie_info(bot: TeleBot, chat_id: int, movie: dict):
    """Вывод информации о фильме для пользователя"""

    genres_str = ", ".join(movie.get("genres", [])) or "Жанры не указаны"

    text = f"*{movie['title']}* ({movie['release_date']})\n" \
           f"🎭 Жанры: {genres_str}\n" \
           f"⭐ Рейтинг: {movie['rating']}\n\n" \
           f"{movie['overview'] or 'Нет описания'}"

    if movie.get("poster_url"):
        bot.send_photo(chat_id=chat_id, photo=movie["poster_url"], caption=text, parse_mode="Markdown")
    else:
        bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")


def get_movie_details_by_id(id_movie: int) -> Optional[dict]:
    """Запрос информации о фильме по его id"""

    # Получаем всю информацию о фильме
    data = make_api_request(f"/movie/{id_movie}", BASE_PARAMS)
    if not data:
        return None

    # Возвращаем словарь с нужными данными
    return {"title": data.get("title"),
            "overview": data.get("overview"),
            "release_date": data.get("release_date", "")[:4],
            "rating": data.get("vote_average"),
            "poster_url": IMG_BASE_URL + data["poster_path"] if data.get("poster_path") else None,
            "genres": [genre["name"] for genre in data.get("genres", [])]}


def search_movie_by_query(query: str) -> Optional[dict]:
    """Поиск фильма по названию"""

    # Получаем информацию о фильме по его названию
    data = make_api_request('/search/movie', params={**BASE_PARAMS, "query": query, "include_adult": False})
    if not data:
        return None

    # Возвращаем None если поиск не дал результатов
    if not data["results"]:
        return None

    # Если фильмов несколько берем первый
    movie = data["results"][0]

    # Возвращаем словарь с отфильтрованными данными о фильме
    return get_movie_details_by_id(movie.get('id'))


def get_movies_by_genre(id_genre: int) -> Optional[list[dict]]:
    """ Функция, осуществляющая поиск фильмов по заданному жанру и фильтрам."""

    params = {**BASE_PARAMS,
              "sort_by": "vote_average.desc",
              "vote_count.gte": 1000,
              "vote_average.gte": 7.0,
              "primary_release_date.gte": "1990-01-01",
              "with_genres": str(id_genre),
              "page": 1}

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

    # Рандомно выбираем из них 5 уникальных фильмов
    movies = sample(movie_list, min(5, len(movie_list)))

    # Записываем отфильтрованные данные в список и выводим его
    result = []
    for movie in movies:
        result.append(get_movie_details_by_id(movie.get('id')))
    return result
