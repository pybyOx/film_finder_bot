from telebot.types import Message
from loader import bot
from database.models import User
from peewee import IntegrityError


@bot.message_handler(commands=["start"])
def handle_start(message: Message) -> None:
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.full_name

    # Если пользователя нет в базе - заносим и отправляем приветственное сообщение
    try:
        User.create(user_id=user_id,
                    username=username)
        bot.reply_to(message, f"🎬 Привет, {username}! \nЯ FilmBuddy — твой гид по миру кино."
                              f"\nДля просмотра доступных команд напиши /help")
        
    # Иначе приветствуем уже зарегистрированного пользователя
    except IntegrityError:
        bot.reply_to(message, f"Рад вас снова видеть, {username}!")




