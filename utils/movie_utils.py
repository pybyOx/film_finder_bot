from telebot import TeleBot


def send_movie_info(bot: TeleBot, chat_id: int, movie: dict):
    genres_str = ", ".join(movie.get("genres", [])) or "Жанры не указаны"
    text = f"*{movie['title']}* ({movie['release_date']})\n" \
           f"🎭 Жанры: {genres_str}\n" \
           f"⭐ Рейтинг: {movie['rating']}\n\n" \
           f"{movie['overview'] or 'Нет описания'}"

    if movie.get("poster_url"):
        bot.send_photo(chat_id=chat_id, photo=movie["poster_url"], caption=text, parse_mode="Markdown")
    else:
        bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")
