from random import randint, sample
from api.tmdb_api import make_api_request
from utils.exceptions import MovieNotFoundError


def random_movie(params: dict, count: int) -> list[dict]:
    """
    Выбирает нужное количество случайных фильмов по заданным параметрам.

    :arg params: Параметры запроса
    :arg count: Количество нужных случайных фильмов
    :arg: Список с информацией о фильмах
    :raise ResponseError: при ошибке запроса к api
    :raise MovieNotFoundError: если нет результатов поиска
    """

    response = make_api_request('/discover/movie', params)

    # Рандомно выбираем одну страницу
    random_page = randint(1, response.get("total_pages"))
    params["page"] = random_page

    # Получаем с этой страницы все фильмы
    movies_from_page = make_api_request('/discover/movie', params)
    results = movies_from_page.get("results", [])
    if not results:
        raise MovieNotFoundError("Не удалось найти фильмы по заданным параметрам")

    # Рандомно выбираем из них заданное количество уникальных фильмов
    movies = sample(results, min(count, len(results)))
    return movies
