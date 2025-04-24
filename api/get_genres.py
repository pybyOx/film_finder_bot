import json
import os
from datetime import datetime, timedelta
import requests
from config_data.config import RAPID_API_KEY, BASE_URL, GENRES_CACHE_FILE
from api.error_handling import error_handling


def fetch_genres_from_api():
    response = requests.get(f"{BASE_URL}/genre/movie/list", params={"api_key": RAPID_API_KEY,
                                                                    "language": "ru-RU"})
    if not error_handling(response):
        return None

    genres_data = response.json()["genres"]
    return {genre["name"].lower(): genre["id"] for genre in genres_data}


def get_genres():
    if os.path.exists(GENRES_CACHE_FILE):
        with open(GENRES_CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            updated_at = datetime.fromisoformat(data["updated_at"])
            if datetime.now() - updated_at < timedelta(days=7):
                return data["genres"]

    genres = fetch_genres_from_api()
    with open(GENRES_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": datetime.now().isoformat(),
            "genres": genres
        }, f, ensure_ascii=False, indent=2)
    return genres
