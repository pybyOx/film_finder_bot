from typing import Dict


def write_genres_data(genres: Dict) -> Dict[str, int]:
    """Функция для записи жанров в нужный формат"""
    genres_list = genres["genres"]
    return {genre["name"].lower(): genre["id"] for genre in genres_list}
