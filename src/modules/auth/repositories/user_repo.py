from sqlalchemy import and_, exists, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.db.models.auth import User


class UserRepository:
    """
    Репозиторий для работы с моделью пользователя.
    """

    def __init__(self, session: AsyncSession):
        """
        Инициализация сессии SQLAlchemy.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
        """
        self.session = session

    async def get_by_fields(self, **kwargs) -> User | None:
        """
        Получить пользователя по полям (например, username, email).

        Args:
            **kwargs: Произвольные поля модели User.

        Returns:
            User | None: Найденный пользователь или None.

        Raises:
            ValueError: Если поле не существует в модели.
        """

        conditions = []
        for key, value in kwargs.items():
            if hasattr(User, key):
                conditions.append(getattr(User, key) == value)
            else:
                raise ValueError(f"Invalid field: {key}")

        stmt = select(User).where(and_(*conditions))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_fields(self, **kwargs) -> bool:
        """
        Проверить, существует ли пользователь по указанным полям.

        Args:
            **kwargs: Произвольные поля модели User.

        Returns:
            bool: True, если пользователь существует, иначе False.

        Raises:
            ValueError: Если поле не существует в модели.
        """
        conditions = []
        for key, value in kwargs.items():
            if hasattr(User, key):
                conditions.append(getattr(User, key) == value)
            else:
                raise ValueError(f"Invalid field: {key}")

        stmt = select(exists().where(or_(*conditions)))
        result = await self.session.execute(stmt)
        return result.scalar()

    # async def update_user_by_id(self, user_id: int, data: dict) -> Optional[User]:
    #     await self.session.execute(
    #         update(User).where(User.id == user_id).values(**data)
    #     )
    #     await self.session.commit()
    #     return await self.get_by_fields(id=user_id)

    async def create(self, user_data: dict, hashed_password: str) -> User:
        """
        Создание нового пользователя.

        Args:
            user_data (UserCreateSchema): Данные для создания пользователя.
            hashed_password (str): Хэш пароля.

        Returns:
            User: Созданный пользователь.
        """
        user = User(**user_data, hashed_password=hashed_password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
