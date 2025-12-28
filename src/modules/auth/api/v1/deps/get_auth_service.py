# src/modules/auth/api/v1/deps/get_auth_service.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.api.v1.services.auth_service import AuthService
from src.modules.auth.repositories.jwt_repo import JWTRepo
from src.modules.auth.repositories.user_repo import UserRepository
from src.shared.configs.get_settings import get_settings
from src.shared.db.session import get_async_session
from src.shared.deps.get_redis_service import get_redis_service
from src.shared.services.redis_service import RedisService


async def get_auth_service(
    db: AsyncSession = Depends(get_async_session),
    redis_service: RedisService = Depends(get_redis_service),
) -> AuthService:
    """
    Собрать экземпляр `AuthService` с инфраструктурными зависимостями.

    Args:
        db (AsyncSession): Асинхронная сессия базы данных.
        redis_service (RedisService): Клиент Redis для хранения access токенов.

    Returns:
        AuthService: Готовый к использованию сервис авторизации.
    """
    return AuthService(
        user_repo=UserRepository(db),
        jwt_repo=JWTRepo(db),
        redis_service=redis_service,
        settings=get_settings(),
    )
