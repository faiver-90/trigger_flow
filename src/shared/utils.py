import time

import requests


def ping_resource(url: str, max_retries: int = 3, delay: float = 1.0) -> bool:
    """
    Пингует ресурс по URL с ограниченным числом попыток.

    :param url: URL ресурса
    :param max_retries: максимальное количество попыток
    :param delay: задержка между попытками (в секундах)
    :return: True, если ответ получен с кодом 200, иначе False
    """
    for _ in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass
        time.sleep(delay)
    return False
