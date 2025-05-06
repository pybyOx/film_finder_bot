from database.models import is_movie_favorite
from telebot.types import InlineKeyboardButton, CallbackQuery
from loader import bot
from database.models import FavoriteMovie, User
from .pagination_state import user_pages
from keyboards.inline.combined_keyboard import get_combined_keyboard


def get_favorite_button(user_id: int, movie_id: int) -> InlineKeyboardButton:
    """Возвращает кнопку добавления или удаления фильма из избранного.
    Если фильм уже в избранном у пользователя — возвращается кнопка "♥" (удалить),
    иначе — кнопка "♡" (добавить).

    :param user_id: ID пользователя Telegram
    :param movie_id: Уникальный ID фильма
    :return: InlineKeyboardButton — готовая кнопка
    """
    if is_movie_favorite(user_id, movie_id):
        return InlineKeyboardButton("♥", callback_data=f"remove_fav:{movie_id}")
    return InlineKeyboardButton("♡", callback_data=f"add_fav:{movie_id}")


@bot.callback_query_handler(func=lambda call: call.data.startswith(("add_fav:", "remove_fav:")))
def handle_favorite(call: CallbackQuery):
    """Обработчик кнопок добавить в избранное/удалить из избранного"""

    user_id = call.from_user.id
    user = User.get(User.user_id == user_id)
    action, movie_id = call.data.split(":")
    movie_id = int(movie_id)

    data = user_pages.get(user_id)
    index = data["current_index"]
    movies = data["movies"]
    total = len(movies)
    movie = movies[index]
    is_favorites = data["is_favorites"]

    if action == "add_fav":

        FavoriteMovie.create(
            movie_id=movie_id,
            user=user,
            title=movie["title"],
            overview=movie["overview"],
            rating=movie["rating"],
            year=movie["release_date"],
            genre=movie.get("genres", []),
            poster_url=movie.get("poster_url")
        )
        message = "Добавлено в избранное."
    else:
        movie = FavoriteMovie.get((FavoriteMovie.user == user) & (FavoriteMovie.movie_id == movie_id))
        movie.delete_instance()
        message = "Удалено из избранного."

    updated_keyboard = get_combined_keyboard(user_id, movie, total, index, is_favorites)

    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=updated_keyboard)

    bot.answer_callback_query(call.id, message)
