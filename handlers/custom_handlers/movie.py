from telebot.types import Message
from loader import bot
from utils.check_name import check_name
from utils.movie_utils import send_movie_info, search_movie_by_query


@bot.message_handler(commands=["movie"])
def movie_handler(message: Message):
    """Обработчик команды |movie"""

    # Проверка ввел ли пользователь название фильма
    movie_name = check_name(message, '/movie Интерстеллар')
    if movie_name is None:
        return

    # Получаем словарь с данными о фильме
    movie = search_movie_by_query(movie_name)

    # Если фильм найден выводим данные о нем
    if movie:
        send_movie_info(bot, message.chat.id, movie)
    else:
        bot.send_message(message.chat.id, "Фильм не найден. Попробуйте другое название.")
