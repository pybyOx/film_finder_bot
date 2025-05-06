from telebot.types import InlineKeyboardButton, CallbackQuery
from loader import bot
from database.models import FavoriteMovie, User
from keyboards.inline.pagination_state import user_pages
from keyboards.inline.combined_keyboard import get_combined_keyboard


def get_watched_button(movie: FavoriteMovie) -> InlineKeyboardButton:
    """Возвращает кнопку, отражающую статус просмотра фильма.

    Если фильм помечен как просмотренный — кнопка "✅" (снять отметку),
    иначе — кнопка "🔲" (отметить как просмотренный).

    :param movie: Объект фильма из таблицы FavoriteMovie
    :return: InlineKeyboardButton — готовая кнопка
    """
    text: str = "✅" if movie.is_watched else "🔲"
    action: str = "remove_watch" if movie.is_watched else "add_watch"
    callback: str = f"{action}:{movie.movie_id}"
    return InlineKeyboardButton(text, callback_data=callback)


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
