import requests
from config_data.config import BASE_URL
from api.error_handling import error_handling
from typing import Dict, Any


def make_api_request(url_longer: str, params: dict) -> Dict[Any]:
    """Отправляет запрос к API и возвращает результат в виде словаря."""
    response = requests.get(f"{BASE_URL}{url_longer}", params=params)

    # Если возникла ошибка запроса возвращается пустой словарь
    if not error_handling(response):
        return {}

    return response.json()
