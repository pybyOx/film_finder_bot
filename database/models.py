from peewee import (SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField, DateTimeField,
                    TextField, FloatField, BooleanField)
from datetime import datetime

db = SqliteDatabase("favorite.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    username = CharField(null=True)


class FavoriteMovie(BaseModel):
    movie_id = IntegerField()
    user = ForeignKeyField(User, backref="favorite")

    datetime = DateTimeField(default=datetime.now)

    title = CharField()
    overview = TextField()
    rating = FloatField(null=True)
    year = CharField(null=True)
    genres = CharField(null=True)
    poster_url = CharField(null=True)

    is_watched = BooleanField(default=False)

    class Meta:
        indexes = (
            (('user', 'movie_id'), True),
        )


def create_models():
    try:
        db.connect()
        db.create_tables([User, FavoriteMovie], safe=True)
    finally:
        db.close()


def is_movie_favorite(user_id: int, movie_id: int) -> bool:
    return FavoriteMovie.select().where(
        (FavoriteMovie.user == user_id) &
        (FavoriteMovie.movie_id == movie_id)
    ).exists()


def delete_user(user_id: int) -> None:

    # Удалим сначала все избранные фильмы, связанные с пользователем
    FavoriteMovie.delete().where(FavoriteMovie.user == user_id).execute()

    # Удалим самого пользователя
    User.delete().where(User.user_id == user_id).execute()
