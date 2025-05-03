from functools import wraps
from telebot.types import Message
from loader import bot
from database.models import User


def send_typing_action(func):
    """Декоратор, показывающий индикатор набора текста перед обработкой команды."""
    @wraps(func)
    def wrapper(message: Message, *args, **kwargs):
        bot.send_chat_action(message.chat.id, 'typing')
        return func(message, *args, **kwargs)
    return wrapper


def registration_check(func):
    """Декоратор для проверки регистрации пользователя в базе данных"""
    @wraps(func)
    def wrapper(message: Message, *args, **kwargs):
        try:
            User.get(User.user_id == message.from_user.id)
        except User.DoesNotExist:
            bot.reply_to(message, "Сначала введите /start, чтобы зарегистрироваться.")
            return
        return func(message, *args, **kwargs)
    return wrapper
