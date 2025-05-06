from database.models import FavoriteMovie, User
from peewee import IntegrityError


def add_to_favorites(user_id: int, movie_data: dict):
    """Сохраняет фильм в избранное пользователя"""

    try:
        FavoriteMovie.create(
            movie_id=movie_data["id"],
            user=User.get(User.user_id == user_id),
            title=movie_data["title"],
            overview=movie_data.get("overview", ""),
            rating=movie_data.get("rating"),
            year=movie_data.get("release_date"),
            genre=", ".join(movie_data.get("genres", [])) or "Жанры не указаны",
            poster_url=movie_data.get("poster_url")
        )
        return "Фильм добавлен в избранное ✅"

    except IntegrityError:
        return "Этот фильм уже в избранном 💾"

    except Exception as e:
        # На случай других ошибок
        return f"Произошла ошибка при добавлении: {str(e)}"










    FavoriteMovie.create(
        user=User.get(User.user_id == user_id),
        title=movie_data["title"],
        overview=movie_data.get("overview", ""),
        rating=movie_data.get("rating"),
        year=movie_data.get("release_date"),
        genre=", ".join(movie_data.get("genres", [])) or "Жанры не указаны",
        poster_url=movie_data.get("poster_url"))
