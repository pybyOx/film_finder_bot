from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import FavoriteMovie, User
from database.models import is_movie_favorite


def get_combined_keyboard(user_id: int, movie_id: int, total: int, index: int) \
        -> InlineKeyboardMarkup:
    """
    Создаёт комбинированную клавиатуру с пагинацией(если фильмов больше одного) и кнопками

    "♥" (удалить из избранного) - если фильм уже в избранном у пользователя / "♡" (добавить в избранное),
    "✅" (снять отметку) - если фильм помечен как просмотренный / "🔲" (отметить как просмотренный).

    :param user_id: ID пользователя
    :param movie_id: индекс фильма
    :param total: общее количество фильмов (для пагинации)
    :param index: текущий индекс
    :param is_favorite: True, если используется команда /favorites (по умолчанию False)
    :return: InlineKeyboardMarkup"""
    from states.pagination_state import USER_PAGES
    keyboard = InlineKeyboardMarkup(row_width=2)
    row_1 = []
    row_2 = []

    # Кнопки пагинации, если фильмов больше одного
    if total > 1:
        if index > 0:
            row_1.append(InlineKeyboardButton("◀️", callback_data="prev"))
        if index < total - 1:
            row_1.append(InlineKeyboardButton("▶️", callback_data="next"))

        keyboard.row(*row_1)

    # Кнопка "♥"/"♡"
    row_2.append(InlineKeyboardButton("♥", callback_data=f"remove_fav")
                 if is_movie_favorite(user_id, movie_id)
                 else InlineKeyboardButton("🤍", callback_data=f"add_fav"))

    # Кнопка "✅"/"🔲", если это favorites
    if USER_PAGES.get_state(user_id).is_favorite:
        user = User.get(User.user_id == user_id)
        movie = FavoriteMovie.get((FavoriteMovie.user == user) & (FavoriteMovie.movie_id == movie_id))

        text: str = "✅" if movie.is_watched else "🔲"
        action: str = "remove_watch" if movie.is_watched else "add_watch"
        callback: str = f"{action}:{movie.movie_id}"

        row_2.append(InlineKeyboardButton(text, callback_data=callback))

    keyboard.row(*row_2)

    return keyboard
