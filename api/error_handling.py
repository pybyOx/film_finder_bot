import requests


def error_handling(response: requests.Response) -> bool:
    """Обработка ошибок запроса к API"""
    try:
        response.raise_for_status()

    # При возникновении ошибки выводит ее и возвращает False
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return False
    except Exception as e:
        print(f"Other error occurred: {e}")
        return False

    # Если ошибок нет возвращает True
    return True
