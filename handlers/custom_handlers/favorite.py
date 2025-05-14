from telebot.types import Message
from loader import bot
from database.models import User, FavoriteMovie
from utils.decorators import ensure_user_registered, send_typing_action
from models.movie_model import Movie
from states.pagination_state import PageState, USER_PAGES
from config_data.config import IMG_BASE_URL
from utils.get_cache_file import get_genres
from utils.send_movie_info import send_movie_info


@bot.message_handler(commands=["favorites"])
@ensure_user_registered
@send_typing_action
def favorite_handler(message: Message) -> None:
    """Обработчик команды /favorites"""
    message_id = message.message_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    user = User.get(User.user_id == user_id)

    favorites = FavoriteMovie.select().where(FavoriteMovie.user == user).order_by(FavoriteMovie.datetime.desc())
    if not favorites.exists():
        bot.reply_to(message, "Избранных фильмов нет.")
        return

    movies = [Movie({"id": fav.movie_id,
                     "title": fav.title,
                     "release_date": fav.year,
                     "vote_average": fav.rating,
                     "genre_ids": [get_genres()[name] for name in fav.genres.split(', ')],
                     "overview": fav.overview,
                     "poster_path": fav.poster_url.replace(IMG_BASE_URL, '')})
              for fav in favorites]

    state = PageState(movies, is_favorite=True)
    USER_PAGES.set_state(user_id, state)

    send_movie_info(bot, chat_id, user_id, movies[0], state.current_index, state.total())
