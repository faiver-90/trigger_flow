from src.modules.notifications.repository.notification_repo import (
    NotificationRepo,
)
from src.modules.notifications.services.notification_service import (
    CRUDNotificationService,
)
from src.shared.services.base_get_service import base_get_service

get_notification_service = base_get_service(CRUDNotificationService, NotificationRepo)
