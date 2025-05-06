from telebot.types import Message
from loader import bot
from database.models import User, FavoriteMovie
from utils.movie_utils import send_movie_info
from utils.decorators import registration_check, send_typing_action
from keyboards.inline.pagination_state import user_pages, init_user_pages


@bot.message_handler(commands=["favorite"])
@registration_check
@send_typing_action
def favorite_handler(message: Message) -> None:
    """Обработчик команды /favorite"""
    user_id = message.from_user.id
    user = User.get(User.user_id == user_id)

    favorites = FavoriteMovie.select().where(FavoriteMovie.user == user).order_by(FavoriteMovie.datetime.desc())

    if not favorites:
        bot.reply_to(message, "Избранных фильмов нет.")
        return

    movies = [{"id": fav.movie_id,
               "title": fav.title,
               "release_date": fav.release_date,
               "rating": fav.rating,
               "genres": fav.genres.split(", "),
               "overview": fav.overview,
               "poster_url": fav.poster_url}
              for fav in favorites]

    init_user_pages(user.user_id, movies, 0, True)

    send_movie_info(bot, message.chat.id, user_id, movies[0], len(movies))
