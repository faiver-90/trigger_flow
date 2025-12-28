from datetime import datetime

import pytz


def convert_utc_to_local(
    utc_timestamp: int, timezone_str: str = "Europe/Moscow"
) -> str:
    """
    Переводит UTC timestamp в локальное время (по указанному часовому поясу).

    :param utc_timestamp: Время в формате Unix timestamp (в секундах).
    :param timezone_str: Название часового пояса (например, "Europe/Moscow", "Asia/Cairo").
    :return: Строка с датой и временем в формате "%Y-%m-%d %H:%M:%S".
    """
    utc_dt = datetime.utcfromtimestamp(utc_timestamp).replace(tzinfo=pytz.utc)
    local_dt = utc_dt.astimezone(pytz.timezone(timezone_str))
    return local_dt.strftime("%Y-%m-%d %H:%M:%S")
