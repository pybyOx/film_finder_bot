from telebot.types import CallbackQuery
from loader import bot
from .pagination_state import user_pages
from database.models import FavoriteMovie, User
from keyboards.inline.combined_keyboard import get_combined_keyboard


@bot.callback_query_handler(func=lambda call: call.data in ["prev", "next"])
def handle_pagination(call: CallbackQuery):
    """Обработчик кнопок вперед-назад"""

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # Получаем данные из хранилища состояния пользователя
    data = user_pages.get(user_id)
    if not data:
        bot.answer_callback_query(call.id, "Нет данных.")
        return

    # Обновляем индекс в зависимости от действия
    if call.data == "prev" and data["current_index"] > 0:
        data["current_index"] -= 1
    elif call.data == "next" and data["current_index"] < len(data["movies"]) - 1:
        data["current_index"] += 1

    # Удаляем клавиатуру
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

    # Получаем текущий фильм
    index: int = data["current_index"]
    movie: dict = data["movies"][index]
    total: int = len(data["movies"])
    is_favorites: bool = data.get("is_favorites", False)

    from utils.movie_utils import send_movie_info
    # Показываем фильм с актуальной клавиатурой
    send_movie_info(bot, chat_id, user_id, movie, total, index, is_favorites)

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith(("add_watch:", "remove_watch:")))
def handle_favorite(call: CallbackQuery):
    """Обработчик кнопок просмотрено/не просмотрено"""
    user_id = call.from_user.id
    user = User.get(User.user_id == user_id)
    action, movie_id = call.data.split(":")
    movie_id = int(movie_id)

    # Обновляем статус просмотра фильма
    movie = FavoriteMovie.get((FavoriteMovie.user == user) & (FavoriteMovie.movie_id == movie_id))
    movie.is_watched = (action == "add_watch")
    movie.save()

    # Получаем данные из пагинационного состояния
    data: dict = user_pages.get(user_id)
    movies: list = data["movies"]
    index = data["current_index"]
    total = len(movies)
    is_favorites = data.get("is_favorites", False)

    # Пересоздаём клавиатуру
    updated_keyboard = get_combined_keyboard(user_id, movies[index], total, index, is_favorites)

    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=updated_keyboard)

    bot.answer_callback_query(call.id, "Статус обновлён.")


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
