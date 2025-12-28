from abc import ABC, abstractmethod


class BaseTypeNotificationClass(ABC):
    @abstractmethod
    async def send(self, payload: dict, config: dict): ...

    @classmethod
    @abstractmethod
    def describe(cls) -> dict: ...

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.describe()}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.describe()}>"
