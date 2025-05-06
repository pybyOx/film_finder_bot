from telebot.types import InlineKeyboardMarkup
from .favorite_keyboard import get_favorite_button
from .watched_keyboard import get_watched_button
from .pagination_keyboard import get_pagination_button
from database.models import FavoriteMovie, User


def get_combined_keyboard(user_id: int, movie: dict, total: int, index: int, is_favorites=False) \
        -> InlineKeyboardMarkup:
    """Создаёт комбинированную клавиатуру с пагинацией и кнопками "в избранное" / "просмотрено".
    :param user_id: ID пользователя
    :param movie: словарь фильма (dict)
    :param total: общее количество фильмов (для пагинации)
    :param index: текущий индекс
    :param is_favorites: True, если используется команда /favorites (по умолчанию False)
    :return: InlineKeyboardMarkup"""

    keyboard = InlineKeyboardMarkup(row_width=2)

    # Кнопки пагинации, если фильмов больше одного
    if total > 1:
        keyboard.row(*get_pagination_button(index=index, length=total))

    # Ряд кнопок "♥/♡" и "✅/🔲"
    buttons = []

    # Кнопка "♥"/"♡"
    buttons.append(get_favorite_button(user_id=user_id, movie_id=movie["id"]))

    # Кнопка "✅"/"🔲", если это favorites
    if is_favorites:
        buttons.append(get_watched_button(FavoriteMovie.get((FavoriteMovie.user == User.get(User.user_id == user_id))
                                                            & (FavoriteMovie.movie_id == movie["id"]))))
    keyboard.row(*buttons)

    return keyboard
