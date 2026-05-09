import json
import os
from datetime import datetime, timedelta
from typing import Callable, Dict
from api.tmdb_api import make_api_request
from utils.random_movie import random_movie
from config_data.config import GENRES_CACHE_FILE, BASE_PARAMS, MOVIE_OF_DAY_CACHE


async def get_cache_file(file_path: str, period: int, func_for_create_data: Callable,
                         func_for_write_data: Callable = None, *args) -> dict:
    """
    Создает кэш с данными, проверяет его актуальность и обновляет с указанной периодичностью.

    :arg file_path: Путь до кэш-файла
    :arg period: Периодичность перезаписи кэш-файла в днях
    :arg func_for_create_data: Функция, возвращающая информацию, которая будет записана в кэш-файл
    :arg func_for_write_data: Функция, приводящая информацию в формат словаря
    :return: Словарь с данными о фильме.
    :raise ResponseError: Ошибка запроса к api
    """

    # Если кэш-файл есть и данные актуальны, возвращает словарь с данными
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            updated_at = datetime.fromisoformat(data["updated_at"])
            if datetime.now() - updated_at < timedelta(days=period) and data.get("data"):
                return data["data"]

    # Иначе делает новый запрос,
    data = await func_for_create_data(*args)

    # из него берет нужные данные для записи,
    if func_for_write_data:
        new_data = func_for_write_data(data)
    else:
        new_data = data[0]

    # обновляет данные в кэш-файле
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": datetime.now().isoformat(),
            "data": new_data
        }, f, ensure_ascii=False, indent=4)

    # и возвращает словарь с данными
    return new_data


async def get_genres() -> dict:
    """Получает данные о жанрах из кэша
    :return: Словарь жанров вида {name: id}
    :raise ResponseError: Ошибка запроса к api"""

    return await get_cache_file(GENRES_CACHE_FILE, 7, make_api_request, write_genres_data,
                          "/genre/movie/list", BASE_PARAMS)


def write_genres_data(genres: Dict) -> Dict[str, int]:
    """Функция для записи жанров в нужный формат"""
    genres_list = genres["genres"]
    return {genre["name"].lower(): genre["id"] for genre in genres_list}


async def get_movie_of_day() -> dict:
    """Получает данные о фильме дня из кэша
    :return: Словарь с данными фильма
    :raise ResponseError: Ошибка запроса к api"""
    params = {**BASE_PARAMS,
              "vote_count.gte": 1000,
              "vote_average.gte": 8.0,
              "primary_release_date.gte": "1990-01-01",
              "page": 1}
    movie = await get_cache_file(MOVIE_OF_DAY_CACHE, 1, random_movie, None, params, 1)
    return movie
