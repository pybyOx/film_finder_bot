from telebot.types import CallbackQuery
from loader import bot
from .pagination_state import get_data_from_user_pages
from database.models import FavoriteMovie, User
from keyboards.inline.combined_keyboard import get_combined_keyboard


@bot.callback_query_handler(func=lambda call: call.data in ["prev", "next"])
def handle_pagination(call: CallbackQuery):
    """Обработчик кнопок вперед-назад"""
    from utils.movie_utils import send_movie_info
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # Получаем данные из user_pages
    data, movies, index, movie, total, is_favorite = get_data_from_user_pages(user_id)

    # Обновляем индекс в зависимости от действия
    if call.data == "prev" and index > 0:
        data["current_index"] -= 1
    elif call.data == "next" and index < total - 1:
        data["current_index"] += 1

    send_movie_info(bot, chat_id, user_id, message_id=call.message.message_id)

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith(("add_watch:", "remove_watch:")))
def handle_watched(call: CallbackQuery):
    """Обработчик кнопок просмотрено/не просмотрено"""

    user_id = call.from_user.id
    user = User.get(User.user_id == user_id)

    action, movie_id = call.data.split(":")
    movie_id = int(movie_id)

    # Обновляем статус просмотра фильма
    movie = FavoriteMovie.get((FavoriteMovie.user == user) & (FavoriteMovie.movie_id == movie_id))
    movie.is_watched = (action == "add_watch")
    movie.save()

    # Получаем данные из user_pages
    data, movies, index, movie, total, is_favorite = get_data_from_user_pages(user_id)

    # Пересоздаём клавиатуру
    updated_keyboard = get_combined_keyboard(user_id, movie, total, index, is_favorite)

    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=updated_keyboard)

    bot.answer_callback_query(call.id, "Статус обновлён.")


@bot.callback_query_handler(func=lambda call: call.data.startswith(("add_fav:", "remove_fav:")))
def handle_favorite(call: CallbackQuery):
    """Обработчик кнопок добавить в избранное/удалить из избранного"""
    from utils.movie_utils import send_movie_info

    user_id = call.from_user.id
    user = User.get(User.user_id == user_id)
    action, movie_id = call.data.split(":")
    movie_id = int(movie_id)
    try:
        data, movies, index, movie, total, is_favorite = get_data_from_user_pages(user_id)

        if action == "add_fav":

            FavoriteMovie.create(
                movie_id=movie_id,
                user=user,
                title=movie["title"],
                overview=movie["overview"],
                rating=movie["rating"],
                year=movie["year"],
                genres=movie.get("genres", ""),
                poster_url=movie.get("poster_url")
            )
            message = "Добавлено в избранное."

            updated_keyboard = get_combined_keyboard(user_id, movie, total, index)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          reply_markup=updated_keyboard)
        else:
            # Удаление фильма из FavoriteMovie
            FavoriteMovie.get((FavoriteMovie.user == user) & (FavoriteMovie.movie_id == movie_id)).delete_instance()
            message = "Удалено из избранного."

            # Удаляем фильм из user_pages
            del data["movies"][index]

            # Обновляем current_index, если нужно
            if data["movies"]:
                if index >= len(data["movies"]):
                    data["current_index"] = max(0, len(data["movies"]) - 1)

                # Показываем следующий фильм
                send_movie_info(bot, call.message.chat.id, user_id,
                                message_id=call.message.message_id, is_favorite=True)
            else:
                bot.send_message(call.message.chat.id, "Избранных фильмов нет.")

        bot.answer_callback_query(call.id, message)

    except TypeError:
        print("Нет данных о фильме в user_pages")
