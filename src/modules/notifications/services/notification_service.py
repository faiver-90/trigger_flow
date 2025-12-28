from src.modules.notifications.repository.notification_repo import (
    NotificationRepo,
)
from src.shared.services.base_crud_service import BaseCRUDService


class CRUDNotificationService(BaseCRUDService[NotificationRepo]):
    pass
