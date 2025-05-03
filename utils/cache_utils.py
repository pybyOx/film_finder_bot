import json
import os
from datetime import datetime, timedelta
from typing import Optional, Callable


def get_cache_file(file_path: str, period: int, func_for_create_data: Callable, func_for_write_data: Callable, *args) \
        -> Optional[dict]:
    """Создает кэш с данными, проверяет его актуальность и обновляет с указанной периодичностью
    Args:
        file_path(str): Путь до кэш-файла
        period(int): Периодичность перезаписи кэш-файла в днях
        func_for_create_data(Callable): Функция, возвращающая информацию, которая будет записана в кэш-файл
        func_for_write_data(Callable): Функция, приводящая информацию в формат словаря
    Return:
        dict: Возвращает словарь с данными о фильме
    """

    # Если кэш-файл есть и данные актуальны, возвращает словарь с данными
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            updated_at = datetime.fromisoformat(data["updated_at"])
            if datetime.now() - updated_at < timedelta(days=period) and data.get("data"):
                return data["data"]

    # Иначе делает новый запрос,
    data = func_for_create_data(*args)
    if not data:
        return None

    # из него берет нужные данные для записи,
    new_data: dict = func_for_write_data(data)

    # обновляет данные в кэш-файле
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": datetime.now().isoformat(),
            "data": new_data
        }, f, ensure_ascii=False, indent=4)

    # и возвращает словарь с данными
    return new_data
