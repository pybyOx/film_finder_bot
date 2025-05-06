from peewee import (SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField, DateTimeField,
                    TextField, FloatField, BooleanField)
from datetime import datetime

db = SqliteDatabase("favorite.db")


class BaseModel(Model):
    class Meta:
        database = db
        indexes = (
            (('user', 'movie_id'), True),  # уникальная пара (user, movie_id)
        )


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
    year = IntegerField(null=True)
    genre = CharField(null=True)
    poster_url = CharField(null=True)

    is_watched = BooleanField(default=False)


def create_models():
    try:
        db.connect()
        db.create_tables(BaseModel.__subclasses__(), safe=True)
    finally:
        db.close()


def is_movie_favorite(user_id: int, movie_id: int) -> bool:
    return FavoriteMovie.select().where(
        (FavoriteMovie.user == user_id) &
        (FavoriteMovie.movie_id == movie_id)
    ).exists()


movie = FavoriteMovie
