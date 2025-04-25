from telebot.types import Message
from loader import bot
from api import tmdb_api
from utils.check_name import check_name
from utils.movie_utils import send_movie_info


@bot.message_handler(commands=["movie"])
def movie_handler(message: Message):

    movie_name = check_name(message, '/movie Интерстеллар')
    if movie_name is None:
        return

    movie = tmdb_api.search_movie(movie_name)

    if movie:
        send_movie_info(bot, message.chat.id, movie)
    else:
        bot.send_message(message.chat.id, "Фильм не найден. Попробуйте другое название.")
