from email.message import EmailMessage

import aiosmtplib

from src.modules.notifications.types.base_type_notify_class import (
    BaseTypeNotificationClass,
)
from src.shared.configs.get_settings import get_settings

settings = get_settings()


class EmailNotification(BaseTypeNotificationClass):
    """
    Сервис отправки email по SMTP.
    Конфигурация берётся из глобальных настроек приложения (settings).
    """

    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_username
        self.smtp_pass = settings.smtp_password
        self.from_email = settings.from_email or self.smtp_user

    async def send(self, payload: dict, config: dict):
        """
        Args:
            payload: данные от триггера (игнорируются здесь).
            config: конфиг из БД, пример:
                {
                    "email": "user@example.com"
                }
        """
        if not self.smtp_host:
            print("[!] SMTP host is not configured")
            return

        recipient = config.get("email")
        if not recipient:
            print("[!] Email is not specified in config")
            return

        subject = "Оповещение от trigger flow"
        body = f"{payload}, {config}"

        message = EmailMessage()
        message["From"] = self.from_email or ""
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        try:
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_pass,
                start_tls=True,
            )
            print(f"[+] Email was send: {recipient}")
        except Exception as exc:  # noqa: BLE001
            print(f"[!] Error sending email: {exc}")

    def describe(self) -> dict:
        return {
            "description": "Отправляет email.",
            "notification_config": {
                "email": "Email получателя",
            },
        }
