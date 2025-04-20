from telebot.types import Message
from loader import bot


@bot.message_handler(func=lambda message: message.text.lower() in ['hello-world', 'start', 'привет',
                                                                   'добрый день', 'здравствуй'])
def bot_start(message: Message):
    bot.reply_to(message, f"🎬 Привет, {message.from_user.full_name}! \nЯ FilmBuddy — твой гид по миру кино."
                          f"\nДля просмотра доступных команд напиши /help")
