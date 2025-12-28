from src.modules.notifications.types.base_type_notify_class import (
    BaseTypeNotificationClass,
)


class ConsoleNotification(BaseTypeNotificationClass):
    async def send(self, payload: dict, config: dict):
        print(f"Notify console with payload {payload}, config {config}")

    @classmethod
    def describe(cls) -> dict:
        return {"descriptions": "Выводит в консоль оповещение"}
