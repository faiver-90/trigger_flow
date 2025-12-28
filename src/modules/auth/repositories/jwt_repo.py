from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.api.v1.schemas import JWTCreateSchema
from src.shared.configs.get_settings import get_settings
from src.shared.db.models.auth import RefreshToken

settings = get_settings()


class JWTRepo:
    """
    Репозиторий для работы с refresh токенами в базе данных.
    """

    def __init__(self, session: AsyncSession):
        """
        Инициализация сессии SQLAlchemy.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
        """
        self.session = session

    async def create(self, jwt_data: JWTCreateSchema):
        """
        Создать и сохранить refresh токен.

        Args:
            jwt_data (JWTCreateSchema): Данные токена.

        Returns:
            RefreshToken: Созданный токен.
        """
        expires_at = (
            datetime.now(timezone.utc) + timedelta(days=settings.refresh_expire_days)
        ).replace(tzinfo=None)

        jwt = RefreshToken(
            user_id=jwt_data.user_id,
            token=jwt_data.token,
            expires_at=expires_at,
            revoked=False,
        )

        self.session.add(jwt)
        await self.session.commit()
        await self.session.refresh(jwt)

        return jwt
