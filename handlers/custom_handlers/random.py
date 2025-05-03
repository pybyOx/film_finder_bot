from telebot.types import Message
from utils.movie_utils import send_movie_info, random_movie, get_movie_details_by_id
from loader import bot
from config_data.config import BASE_PARAMS
from utils.decorators import registration_check, send_typing_action


@bot.message_handler(commands=["random"])
@registration_check
@send_typing_action
def movie_handler(message: Message) -> None:
    """Обработчик команды |random"""

    # Получаем словарь с данными фильма дня
    movie = random_movie({**BASE_PARAMS,
                          "vote_count.gte": 5000,
                          "vote_average.gte": 7.2,
                          "primary_release_date.gte": "1990-01-01",
                          "page": 1}, 1)
    if movie is None:
        bot.send_message(message.chat.id, "Не удалось получить случайный фильм.")
        return

    send_movie_info(bot, message.chat.id, get_movie_details_by_id(movie[0].get('id')))
