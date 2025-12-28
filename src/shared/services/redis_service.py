import redis.asyncio as redis


class RedisService:
    """
    Сервис для работы с Redis — используется для хранения access токенов.
    """

    def __init__(self, client: redis.Redis):
        """
        Инициализация Redis клиента.

        Args:
            url (str): URL подключения к Redis.
        """
        self.client = client

    async def get(self, key: str) -> str | None:
        """
        Получить значение по ключу из Redis.

        Args:
            key (str): Ключ.

        Returns:
            Optional[str]: Значение или None.
        """
        return await self.client.get(key)

    async def set(self, key: str, value: str, ex: int = 3600):
        """
        Установить значение по ключу с истечением срока действия.

        Args:
            key (str): Ключ.
            value (str): Значение.
            ex (int): Время жизни ключа в секундах.
        """
        await self.client.set(key, value, ex=ex)

    async def delete(self, key: str):
        """
        Удалить ключ из Redis.

        Args:
            key (str): Ключ.
        """
        await self.client.delete(key)

    async def exists(self, key: str):
        """
        Проверить, существует ли ключ в Redis.

        Args:
            key (str): Ключ.

        Returns:
            bool: True, если существует, иначе False.
        """
        return await self.client.exists(key) == 1


# redis_service = RedisService(url="redis://redis:6379/0")
