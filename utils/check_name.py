from telebot.types import Message
from utils.exceptions import ArgumentError


def check_name(message: Message, example: str = "") -> str:
    """Извлекает аргумент после команды.
    Если аргумент отсутствует — отправляет пользователю подсказку и возвращает None.
    :arg message: Сообщение пользователя
    :arg example: Пример правильного ввода команды (по умолчанию пустая строка)
    :return: Название фильма/жанра
    :raise ArgumentError: Если пользователь не ввел название фильма/жанра
    """
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        raise ArgumentError(f"Пожалуйста, укажите название. Пример:\n{example}" if example
                            else "Пожалуйста, укажите название после команды.")

    return args[1]
