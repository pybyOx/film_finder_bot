from telebot.types import Message
from loader import bot
from database.models import User, FavoriteMovie
from utils.movie_utils import send_movie_info
from utils.decorators import ensure_user_registered, send_typing_action


@bot.message_handler(commands=["favorites"])
@ensure_user_registered
@send_typing_action
def favorite_handler(message: Message) -> None:
    """Обработчик команды /favorites"""
    user_id = message.from_user.id
    user = User.get(User.user_id == user_id)

    favorites = FavoriteMovie.select().where(FavoriteMovie.user == user).order_by(FavoriteMovie.datetime.desc())
    if not favorites:
        bot.reply_to(message, "Избранных фильмов нет.")
        return

    movies = [{"movie_id": fav.movie_id,
               "title": fav.title,
               "year": fav.year,
               "rating": fav.rating,
               "genres": fav.genres,
               "overview": fav.overview,
               "poster_url": fav.poster_url}
              for fav in favorites]

    send_movie_info(bot, message.chat.id, user_id, movies, True)
