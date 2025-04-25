from api.get_genres import get_genres
from typing import Optional, Dict


def get_genre_id_by_name(genre_name: str, genres: Dict[str, int]) -> Optional[int]:
    return genres.get(genre_name.lower())
