import requests


def error_handling(response: requests.Response) -> bool:
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return False
    except Exception as e:
        print(f"Other error occurred: {e}")
        return False

    return True
