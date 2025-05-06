user_pages = {}


def init_user_pages(user_id: int, movies: list, index: int = 0, is_favorites: bool = False) -> None:
    """Перезаписывает хранилище состояния пользователя."""
    user_pages[user_id]["movies"] = movies
    user_pages[user_id]["current_index"] = index
    user_pages[user_id]["is_favorites"] = is_favorites
