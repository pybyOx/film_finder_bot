import json
import os
from datetime import datetime, timedelta
from config_data.config import GENRES_CACHE_FILE, BASE_PARAMS
from api.tmdb_api import make_api_request
from typing import Optional, Dict


def get_genres() -> Optional[Dict[str, int]]:
    """Создает кэш жанров, проверяет его актуальность, обновляет раз в неделю"""

    # Если кэш-файл есть и данные в нём не старше 7 дней, возвращает словарь с жанрами
    if os.path.exists(GENRES_CACHE_FILE):
        with open(GENRES_CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            updated_at = datetime.fromisoformat(data["updated_at"])
            if datetime.now() - updated_at < timedelta(days=7):
                return data["genres"]

    # Иначе делает новый запрос,
    genres = make_api_request("/genre/movie/list", BASE_PARAMS)
    if not genres:
        return None

    # обновляет данные в кэш-файле
    with open(GENRES_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": datetime.now().isoformat(),
            "genres": {genre["name"].lower(): genre["id"] for genre in genres["genres"]}
        }, f, ensure_ascii=False, indent=4)

    # и возвращает словарь вида {"название жанра": id}
    return genres
