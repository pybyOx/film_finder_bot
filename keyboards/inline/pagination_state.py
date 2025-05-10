from typing import Optional, Any


user_pages = {}


def init_user_pages(user_id: int, movies: list[dict], index: int = 0, is_favorite: bool = False) -> None:
    """Перезаписывает хранилище состояния пользователя."""
    user_pages[user_id]["movies"] = movies
    user_pages[user_id]["current_index"] = index
    user_pages[user_id]["is_favorite"] = is_favorite


def get_data_from_user_pages(user_id: int) -> Optional[Any]:
    """Извлекает данные из хранилища состояния пользователя"""
    data: dict = user_pages.get(user_id)
    movies: list[dict] = data['movies']
    if not movies:
        return None
    index: int = data['current_index']
    movie: dict = movies[index]
    total: int = len(movies)
    is_favorite: bool = data['is_favorite']
    return data, movies, index, movie, total, is_favorite
