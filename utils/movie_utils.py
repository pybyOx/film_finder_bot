from typing import Dict
from config_data.config import IMG_BASE_URL
from telebot import TeleBot


def parse_movie_details(data: Dict):
    return {"title": data.get("title"),
            "overview": data.get("overview"),
            "release_date": data.get("release_date", "")[:4],
            "rating": data.get("vote_average"),
            "poster_url": IMG_BASE_URL + data["poster_path"] if data.get("poster_path") else None,
            "genres": [genre["name"] for genre in data.get("genres", [])]}


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
