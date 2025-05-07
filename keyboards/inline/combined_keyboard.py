from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import FavoriteMovie, User
from database.models import is_movie_favorite


def get_combined_keyboard(user_id: int, movie: dict, total: int, index: int, is_favorites=False) \
        -> InlineKeyboardMarkup:
    """Создаёт комбинированную клавиатуру с пагинацией(если фильмов больше одного) и кнопками
    "♥" (удалить из избранного) - если фильм уже в избранном у пользователя / "♡" (добавить в избранное),
    "✅" (снять отметку) - если фильм помечен как просмотренный / "🔲" (отметить как просмотренный).
    :param user_id: ID пользователя
    :param movie: словарь фильма (dict)
    :param total: общее количество фильмов (для пагинации)
    :param index: текущий индекс
    :param is_favorites: True, если используется команда /favorites (по умолчанию False)
    :return: InlineKeyboardMarkup"""

    keyboard = InlineKeyboardMarkup(row_width=2)

    # Кнопки пагинации, если фильмов больше одного
    if total > 1:

        buttons = []
        if index > 0:
            buttons.append(InlineKeyboardButton("◀️", callback_data="prev"))
        if index < total - 1:
            buttons.append(InlineKeyboardButton("▶️", callback_data="next"))

        keyboard.row(*buttons)

    # Ряд кнопок "♥/♡" и "✅/🔲"
    buttons = []
    movie_id = movie["id"]

    # Кнопка "♥"/"♡"
    buttons.append(InlineKeyboardButton("♥", callback_data=f"remove_fav:{movie_id}")
                   if is_movie_favorite(user_id, movie_id)
                   else InlineKeyboardButton("♡", callback_data=f"add_fav:{movie_id}"))

    # Кнопка "✅"/"🔲", если это favorites
    if is_favorites:
        user = User.get(User.user_id == user_id)
        movie = FavoriteMovie.get((FavoriteMovie.user == user) & (FavoriteMovie.movie_id == movie_id))

        text: str = "✅" if movie.is_watched else "🔲"
        action: str = "remove_watch" if movie.is_watched else "add_watch"
        callback: str = f"{action}:{movie.movie_id}"

        buttons.append(InlineKeyboardButton(text, callback_data=callback))

    keyboard.row(*buttons)

    return keyboard
