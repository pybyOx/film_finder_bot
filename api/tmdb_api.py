import requests
from config_data.config import BASE_URL, BASE_PARAMS, IMG_BASE_URL
from api.error_handling import error_handling
from random import randint
from typing import Optional


def get_movie_details_by_id(id_movie: int) -> Optional[dict]:
    """Запрос информации о фильме по его id"""

    # Получаем всю информацию о фильме
    details = requests.get(f'{BASE_URL}/movie/{id_movie}', params={**BASE_PARAMS})
    if not error_handling(details):
        return None
    data = details.json()

    # Возвращаем словарь с нужными данными
    return {"title": data.get("title"),
            "overview": data.get("overview"),
            "release_date": data.get("release_date", "")[:4],
            "rating": data.get("vote_average"),
            "poster_url": IMG_BASE_URL + data["poster_path"] if data.get("poster_path") else None,
            "genres": [genre["name"] for genre in data.get("genres", [])]}


def search_movie(query: str) -> Optional[dict]:
    """Поиск фильма по названию"""

    # Получаем информацию о фильме по его названию
    response = requests.get(f'{BASE_URL}/search/movie', params={**BASE_PARAMS, "query": query, "include_adult": False})
    if not error_handling(response):  # Проверяем на ошибки запроса
        return None
    data = response.json()

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
              "with_genres": str(id_genre),
              "page": 1}

    # Получаем все фильмы по заданным фильтрам
    first_response = requests.get(f"{BASE_URL}/discover/movie", params=params)
    if not error_handling(first_response):
        return None
    data = first_response.json()

    # Рандомно выбираем одну страницу
    total_pages = min(data.get("total_pages", 1), 20)
    random_page = randint(1, total_pages)
    params["page"] = random_page

    # Получаем с этой страницы первые пять фильмов
    response = requests.get(f"{BASE_URL}/discover/movie", params=params)
    if not error_handling(response):
        return None
    movies = response.json().get("results", [])[:5]

    # Записываем отфильтрованные данные в список и выводим его
    result = []
    for movie in movies:
        result.append(get_movie_details_by_id(movie.get('id')))
    return result
