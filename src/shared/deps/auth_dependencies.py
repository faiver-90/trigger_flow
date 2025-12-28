from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from src.shared.services.jwt_service import decode_token

token_scheme = HTTPBearer()


async def authenticate_user(
    credentials: HTTPAuthorizationCredentials = Depends(token_scheme),
):
    """
    Аутентификация пользователя по JWT токену из заголовка Authorization.

    Args:
        credentials (HTTPAuthorizationCredentials): Данные авторизации (тип и сам токен).

    Returns:
        dict: Расшифрованный payload из токена.

    Raises:
        HTTPException: Если токен некорректен или просрочен.
    """
    token = credentials.credentials
    try:
        return decode_token(token)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(exc)}",
        ) from exc


async def verify_superuser(payload: dict = Depends(authenticate_user)):
    """
    Проверка, что пользователь обладает правами суперпользователя.

    Args:
        payload (dict): Декодированные данные из JWT токена.

    Returns:
        dict: Те же данные payload, если пользователь суперпользователь.

    Raises:
        HTTPException: Если пользователь не является суперпользователем.
    """
    if not payload.get("is_superuser"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is not a superuser"
        )
    return payload


async def get_user_id(user: dict = Depends(authenticate_user)) -> int:
    """Извлечь идентификатор пользователя из расшифрованного JWT payload."""
    return int(user["sub"])
