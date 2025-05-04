from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from loader import bot
from .pagination_state import user_pages
from utils.movie_utils import send_movie_info


def show_movie_page(chat_id: int, user_id: int) -> None:
    """Функция для отображения результатов поиска через пагинацию"""
    print('Функция show_movie_page')
    # Получаем данные из хранилища состояния пользователя
    data: dict = user_pages.get(user_id)

    if not data:
        bot.send_message(chat_id, "Нет данных для отображения.")
        return

    movies: list = data["movies"]
    index: int = data["current_index"]
    movie: dict = movies[index]

    # Кнопки
    keyboard = InlineKeyboardMarkup()
    buttons = []
    if index > 0:
        buttons.append(InlineKeyboardButton("◀️ Назад", callback_data="prev"))
    if index < len(movies) - 1:
        buttons.append(InlineKeyboardButton("Вперёд ▶️", callback_data="next"))
    keyboard.row(*buttons)
    print('Показываем кнопки')
    send_movie_info(bot, chat_id, movie, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ["prev", "next"])
def handle_pagination(call: CallbackQuery):
    """Обработчик кнопок вперед-назад"""

    # Получаем данные из хранилища состояния пользователя
    data = user_pages.get(call.from_user.id)
    if not data:
        bot.answer_callback_query(call.id, "Нет данных.")
        return

    # Меняем индекс
    if call.data == "prev" and data["current_index"] > 0:
        data["current_index"] -= 1
    elif call.data == "next" and data["current_index"] < len(data["movies"]) - 1:
        data["current_index"] += 1

    # Удаляем клавиатуру
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

    show_movie_page(call.message.chat.id, call.from_user.id)
    bot.answer_callback_query(call.id)
