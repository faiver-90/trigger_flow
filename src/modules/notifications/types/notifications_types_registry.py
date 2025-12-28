from src.modules.notifications.types.console import (
    ConsoleNotification,
)
from src.modules.notifications.types.email_notification import (
    EmailNotification,
)

NOTIFY_REGISTRY = {"email": EmailNotification(), "console": ConsoleNotification()}
