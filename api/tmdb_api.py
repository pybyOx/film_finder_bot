import requests
from api.error_handling import error_handling
from typing import Dict, Any
from utils.exceptions import ResponseError


def make_api_request(url_longer: str, params: dict) -> Dict[str, Any]:
    """Отправляет запрос к API и возвращает результат в виде словаря.
    :arg url_longer: Продолжение базового url
    :arg params: Параметры запроса к api
    :return Словарь с результатами запроса
    :raise ResponseError: Ошибка запроса к api
    """
    base_url = "https://api.themoviedb.org/3"
    response = requests.get(f"{base_url}{url_longer}", params=params)

    # Если возникла ошибка запроса возвращается пустой словарь
    if not error_handling(response):
        raise ResponseError("Возникла ошибка запроса к api")

    return response.json()
