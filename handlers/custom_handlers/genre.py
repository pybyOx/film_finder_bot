from telebot.types import Message
from loader import bot
from utils.genre_utils import get_genres
from utils.check_name import check_name
from utils.movie_utils import send_movie_info, get_movies_by_genre


@bot.message_handler(commands=["genre"])
def movie_handler(message: Message):
    """Обработчик команды |genre"""

    # Проверка ввел ли пользователь название жанра
    genre_name = check_name(message, '/genre комедия')
    if genre_name is None:
        return

    # Поиск id введенного жанра из кэша жанров
    genres = get_genres()
    genre_id = genres.get(genre_name.lower())
    if genre_id is None:
        bot.reply_to(message, f"Жанр '{genre_name}' не найден. Убедитесь, что вы ввели его корректно.")
        return

    # Получение списка фильмов по заданному id
    movies = get_movies_by_genre(genre_id)
    if not movies:
        bot.send_message(message.chat.id, f"Не удалось найти фильмы в жанре '{genre_name}'.")
        return

    # Вывод фильмов для пользователя в красивом формате
    for movie in movies:
        send_movie_info(bot, message.chat.id, movie)
