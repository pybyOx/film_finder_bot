from telebot.types import Message
from utils.get_cache_file import get_movie_of_day, get_genres
from loader import bot
from utils.decorators import ensure_user_registered, send_typing_action
from models.movie_model import Movie
from states.pagination_state import PageState, USER_PAGES
from utils.exceptions import ResponseError
from utils.send_movie_info import send_movie_info


@bot.message_handler(commands=["day"])
@ensure_user_registered
@send_typing_action
async def day_handler(message: Message) -> None:
    """Обработчик команды |day"""

    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        # Получаем словарь с данными фильма дня
        movie = await get_movie_of_day()
        genres = await get_genres()

        movie = Movie(movie, genres)

        state = PageState([movie])
        USER_PAGES.set_state(user_id, state)

        send_movie_info(bot, chat_id, user_id, movie, state.current_index, state.total())
    except ResponseError as error:
        bot.send_message(message.chat.id, error)
