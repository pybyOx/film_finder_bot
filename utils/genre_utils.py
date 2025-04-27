import json
import os
from datetime import datetime, timedelta
from config_data.config import GENRES_CACHE_FILE, BASE_PARAMS
from api.tmdb_api import make_api_request
from typing import Optional


def fetch_genres_from_api() -> Optional[dict]:
    genres_data = make_api_request("/genre/movie/list", BASE_PARAMS)
    if not genres_data:
        return None
    genres = genres_data["genres"]
    return {genre["name"].lower(): genre["id"] for genre in genres}


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
