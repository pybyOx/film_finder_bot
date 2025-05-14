class MovieNotFoundError(Exception):
    """Исключение, вызываемое, когда фильм не найден."""
    pass


class ResponseError(Exception):
    """Исключение, вызываемое, когда не удалось получить данные api."""
    pass


class ArgumentError(Exception):
    """Исключение, вызываемое, когда пользователь не ввел название фильма или жанра."""
    pass


class UserPagesError(Exception):
    """Исключение, вызываемое, когда не удается получить данные из user_pages."""
    pass
