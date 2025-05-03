from peewee import (SqliteDatabase, Model, CharField, IntegerField, AutoField, ForeignKeyField, DateTimeField,
                    TextField, FloatField, BooleanField)
from datetime import datetime
import sqlite3

db = SqliteDatabase("history.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    username = CharField()


class Movie(BaseModel):
    search_id = AutoField()
    user = ForeignKeyField(User, backref="history")

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
