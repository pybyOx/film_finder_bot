from telebot.types import InlineKeyboardButton, CallbackQuery
from loader import bot
from .pagination_state import user_pages
from utils.movie_utils import send_movie_info


def get_pagination_button(index: int, length: int) -> list[InlineKeyboardButton]:
    """Возвращает список кнопок для пагинации: "◀️ Назад" и "Вперёд ▶️",
    в зависимости от текущего индекса и длины списка фильмов.

    :param index: Текущий индекс отображаемого фильма (0-based)
    :param length: Общее количество фильмов
    :return: Список из одной или двух InlineKeyboardButton
    """
    buttons = []
    if index > 0:
        buttons.append(InlineKeyboardButton("◀️", callback_data="prev"))
    if index < length - 1:
        buttons.append(InlineKeyboardButton("▶️", callback_data="next"))
    return buttons


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

    # Показываем фильм с актуальной клавиатурой
    send_movie_info(bot, chat_id, user_id, movie, total, index, is_favorites)

    bot.answer_callback_query(call.id)
