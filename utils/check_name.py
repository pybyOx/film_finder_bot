from telebot.types import Message
from loader import bot


def check_name(message: Message, example: str = "") -> str | None:
    """Извлекает аргумент после команды.
    Если аргумент отсутствует — отправляет пользователю подсказку и возвращает None.
    """
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        text = f"Пожалуйста, укажите название. Пример:\n{example}" if example \
            else "Пожалуйста, укажите название после команды."
        bot.reply_to(message, text)
        return None
    return args[1]
