from datetime import datetime, timedelta

from jose import jwt

from src.shared.configs.get_settings import get_settings

settings = get_settings()


def create_token(data: dict, expires_delta: timedelta) -> str:
    """
    Создать JWT токен.

    Args:
        data (dict): Данные для включения в токен.
        expires_delta (timedelta): Время жизни токена.

    Returns:
        str: JWT токен.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_access_token(user_id: str, **data):
    """
    Создать access токен.

    Args:
        user_id (str): Идентификатор пользователя.
        **data: Дополнительные данные (например, is_superuser).

    Returns:
        str: Access токен.
    """

    return create_token(
        {"sub": user_id, **data}, timedelta(minutes=settings.access_expire_min)
    )


def create_refresh_token(user_id: str, **data):
    """
    Создать refresh токен.

    Args:
        user_id (str): Идентификатор пользователя.
        **data: Дополнительные данные.

    Returns:
        str: Refresh токен.
    """
    return create_token(
        {"sub": user_id, **data}, timedelta(days=settings.refresh_expire_days)
    )


def decode_token(token: str):
    """
    Расшифровать и проверить JWT токен.

    Args:
        token (str): JWT токен.

    Returns:
        dict: Расшифрованные данные.

    Raises:
        JWTError: Если токен недействителен или истёк.
    """
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
