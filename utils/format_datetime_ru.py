from config_data.config import MONTHS_RU


def format_datetime_ru(dt):
    return f"{dt.day} {MONTHS_RU[dt.month]} {dt.year}, {dt.strftime('%H:%M')}"
