import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE_URL = "https://image.tmdb.org/t/p/w500"

GENRES_CACHE_FILE = os.path.join(os.path.dirname(__file__), "genres_cache.json")
MOVIE_OF_DAY_CACHE = os.path.join(os.path.dirname(__file__), "movie_of_day_cache.json")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("movie", "Поиск фильма: /movie <название>"),
    ("genre", "Топ-5 фильмов по жанру: /genre <название>"),
    ("day", "Фильм дня"),
    ("random", "Случайный фильм"),
    ("history", "История поиска"),
)

BASE_PARAMS = {"api_key": RAPID_API_KEY,
               "language": "ru-RU"}

MONTHS_RU = {1: "января", 2: "февраля",  4: "апреля", 5: "мая", 6: "июня", 7: "июля", 8: "августа", 9: "сентября",
             10: "октября", 11: "ноября", 12: "декабря"}
