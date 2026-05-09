import httpx
from typing import Dict, Any
from utils.exceptions import ResponseError


async def make_api_request(url_longer: str, params: dict) -> Dict[str, Any]:
    """Отправляет запрос к API и возвращает результат в виде словаря.
    :arg url_longer: Продолжение базового url
    :arg params: Параметры запроса к api
    :return Словарь с результатами запроса
    :raise ResponseError: Ошибка запроса к api
    """
    base_url = "https://api.themoviedb.org/3"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}{url_longer}", params=params)
            response.raise_for_status()
            return response.json()

    except httpx.RequestError as error:
        raise ResponseError(f"Ошибка сети: {error}")

    except httpx.HTTPStatusError as error:
        raise ResponseError(f"Ошибка HTTP {error.response.status_code}: {error}")
