from database.models import Movie, User


def save_movie_to_history(user_id: int, movie_data: dict) -> None:
    """Сохраняет фильм в историю поиска пользователя"""
    Movie.create(
        user=User.get(User.user_id == user_id),
        title=movie_data["title"],
        overview=movie_data.get("overview", ""),
        rating=movie_data.get("rating"),
        year=movie_data.get("release_date"),
        genre=", ".join(movie_data.get("genres", [])) or "Жанры не указаны",
        poster_url=movie_data.get("poster_url"))
