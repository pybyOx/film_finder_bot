from telebot.types import CallbackQuery
from loader import bot
from database.models import FavoriteMovie, User
from keyboards.inline.combined_keyboard import get_combined_keyboard
from utils.exceptions import UserPagesError
from utils.send_movie_info import send_movie_info


@bot.callback_query_handler(func=lambda call: call.data in ["prev", "next"])
def handle_pagination(call: CallbackQuery):
    """Обработчик кнопок вперед-назад"""
    from states.pagination_state import USER_PAGES
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    try:
        state = USER_PAGES.get_state(user_id)

        # Обновляем индекс в зависимости от действия
        if call.data == "prev":
            state.prev()
        elif call.data == "next":
            state.next()

        send_movie_info(bot, chat_id, user_id, state.current_movie(), state.current_index,
                        state.total(), message_id)

        bot.answer_callback_query(call.id)
    except ValueError as error:
        bot.send_message(chat_id, error)
    except UserPagesError as error:
        bot.send_message(chat_id, error)


@bot.callback_query_handler(func=lambda call: call.data.startswith(("add_watch:", "remove_watch:")))
def handle_watched(call: CallbackQuery):
    """Обработчик кнопок просмотрено/не просмотрено"""
    from states.pagination_state import USER_PAGES
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    user = User.get(User.user_id == user_id)

    action, movie_id = call.data.split(":")
    movie_id = int(movie_id)
    try:
        # Обновляем статус просмотра фильма
        movie = FavoriteMovie.get((FavoriteMovie.user == user) & (FavoriteMovie.movie_id == movie_id))
        movie.is_watched = (action == "add_watch")
        movie.save()

        state = USER_PAGES.get_state(user_id)

        # Пересоздаём клавиатуру
        updated_keyboard = get_combined_keyboard(user_id, movie_id, state.total(), state.current_index)

        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=updated_keyboard)

        bot.answer_callback_query(call.id, "Статус обновлён.")
    except UserPagesError as error:
        bot.send_message(chat_id, error)


@bot.callback_query_handler(func=lambda call: call.data.startswith(("add_fav", "remove_fav")))
def handle_favorite(call: CallbackQuery):
    """Обработчик кнопок добавить в избранное/удалить из избранного"""
    from states.pagination_state import USER_PAGES
    message_id = call.message.message_id
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    user = User.get(User.user_id == user_id)

    try:
        state = USER_PAGES.get_state(user_id)
        index = state.current_index
        movie = state.current_movie()
        total = state.total()

        if call.data == "add_fav":

            FavoriteMovie.create(
                movie_id=movie.movie_id,
                user=user,
                title=movie.title,
                overview=movie.overview,
                rating=movie.rating,
                year=movie.year,
                genres=movie.genres,
                poster_url=movie.poster_url
            )
            text = "Добавлено в избранное."

            updated_keyboard = get_combined_keyboard(user_id, movie.movie_id, total, index)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          reply_markup=updated_keyboard)
        else:
            # Удаление фильма из FavoriteMovie
            FavoriteMovie.get((FavoriteMovie.user == user) &
                              (FavoriteMovie.movie_id == movie.movie_id)).delete_instance()
            text = "Удалено из избранного."

            if state.is_favorite:
                # Удаляем фильм из user_pages
                del state.movies[index]

                # Обновляем current_index, если нужно
                if state.movies:
                    if index >= state.total():
                        state.current_index = max(0, state.total() - 1)

                else:
                    bot.delete_message(chat_id=chat_id, message_id=message_id)
                    bot.send_message(chat_id, "Избранных фильмов нет.")

            # Показываем следующий фильм
            send_movie_info(bot, chat_id, user_id, state.current_movie(), state.current_index, state.total(),
                            message_id=message_id)
        bot.answer_callback_query(call.id, text)

    except (UserPagesError, ValueError, Exception) as error:
        print(error)
