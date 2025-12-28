import functools
import logging
from collections.abc import Awaitable
from typing import Any, Callable

from pydantic import BaseModel

errors_logger = logging.getLogger("errors_log")


def log_action(msg: str, logger: logging.Logger):
    """
    Асинхронный декоратор для логирования действий в обработчиках FastAPI или других корутинах.

    Позволяет указывать собственный шаблон сообщения и конкретный логгер,
    в который будет отправлено сообщение после успешного выполнения функции
    (или сообщение об ошибке в случае исключения).

    Аргументы:
        msg (str):
            Шаблон сообщения для логирования.
            Поддерживает подстановку аргументов функции через `.format(**kwargs)`.
            Например: "Update source {source_id} by user {user_id}".
        logger (logging.Logger):
            Объект логгера, в который будет отправлено сообщение.
            Можно использовать разные логгеры для разных частей приложения
            (например, `logging.getLogger("auth")`, `logging.getLogger("access")`).

    Использование:
        import logging
        logger_auth = logging.getLogger("auth")

        @log_action("Попытка логина пользователя {username}", logger_auth)
        async def login(username: str, password: str):
            return {"ok": True}

        # При вызове login(username="vasya", password="123")
        # в логгер "auth" будет записано:
        # INFO:auth:Попытка логина пользователя vasya

    Особенности:
        - Сообщение логируется только после успешного выполнения функции.
        - Если внутри функции произошло исключение, в логгер записывается сообщение
          уровня ERROR с трассировкой стека.
        - Если в шаблоне `msg` указаны переменные, которых нет в kwargs функции,
          они игнорируются, и в лог попадает исходный шаблон.
    """

    def decorator(func: Callable[..., Awaitable[Any]]):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            ctx: dict[str, Any] = dict(kwargs)

            for v in kwargs.values():
                if isinstance(v, BaseModel):
                    ctx.update(v.model_dump(exclude_unset=True))
                elif isinstance(v, dict):
                    ctx.update(v)

            try:
                text = msg.format(**ctx)
            except KeyError:
                text = msg

            try:
                result = await func(*args, **kwargs)
                logger.info(text)
                return result
            except Exception:
                errors_logger.exception(f"Errors in functions -- {func.__name__}")
                raise

        return wrapper

    return decorator
