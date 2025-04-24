from telebot.types import Message
from loader import bot
from api import tmdb_api


@bot.message_handler(commands=["movie"])
def movie_handler(message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        bot.reply_to(message, "Пожалуйста, укажите название фильма. Пример:\n/movie Интерстеллар")
        return

    query = args[1]
    movie = tmdb_api.search_movie(query)

    if movie:
        genres = ", ".join(movie.get("genres", [])) or "Жанры не указаны"
        text = f"*{movie['title']}* ({movie['release_date']})\n" \
               f"🎭 Жанры: {genres}\n" \
               f"⭐ Рейтинг: {movie['rating']}\n\n" \
               f"{movie['overview'] or 'Нет описания'}"

        if movie["poster_url"]:
            bot.send_photo(chat_id=message.chat.id, photo=movie["poster_url"], caption=text, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, text, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "Фильм не найден. Попробуйте другое название.")
