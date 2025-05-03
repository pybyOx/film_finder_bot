from telebot.types import Message
from loader import bot
from database.models import User, Movie
from utils.movie_utils import send_movie_info
from utils.decorators import registration_check, send_typing_action


@bot.message_handler(commands=["history"])
@registration_check
@send_typing_action
def handle_history(message: Message) -> None:
    """Обработчик команды /history"""

    user = User.get(User.user_id == message.from_user.id)

    movies = Movie.select().where(Movie.user == user).order_by(Movie.datetime.desc())

    if not movies:
        bot.reply_to(message, "История поиска пуста.")
        return

    for movie in movies[:5]:  # Пока ограничим вывод до 5 записей
        send_movie_info(bot, message.chat.id, {"title": movie.title,
                                               "overview": movie.overview,
                                               "rating": movie.rating,
                                               "release_date": movie.year,
                                               "genres": movie.genre.split(", ") if movie.genre else [],
                                               "poster_url": movie.poster_url,
                                               "datetime": movie.datetime})
