from functools import wraps
from telebot.types import Message
from database.models import User
from peewee import IntegrityError
from loader import bot


def ensure_user_registered(func):
    """Декоратор для регистрации новых пользователей"""

    @wraps(func)
    def wrapper(message, *args, **kwargs):
        user_id = message.from_user.id
        username = message.from_user.full_name

        try:
            User.create(user_id=user_id, username=username)
            bot.send_message(message.chat.id,
                             f"🎬 Привет, {username}! \nЯ FilmBuddy — твой гид по миру кино.\n"
                             f"Для просмотра доступных команд напиши /help")
        except IntegrityError:
            pass  # Пользователь уже есть в базе

        return func(message, *args, **kwargs)
    return wrapper


def send_typing_action(func):
    """Декоратор, показывающий индикатор набора текста перед обработкой команды."""

    @wraps(func)
    def wrapper(message: Message, *args, **kwargs):
        bot.send_chat_action(message.chat.id, 'typing')
        return func(message, *args, **kwargs)
    return wrapper
