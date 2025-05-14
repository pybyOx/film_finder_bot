from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot
from utils.decorators import ensure_user_registered


@bot.message_handler(commands=["help"])
@ensure_user_registered
def bot_help(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, f"\nДоступные команды:\n\n{"\n".join(text)}")
