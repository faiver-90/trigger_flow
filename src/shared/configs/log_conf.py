from logging.config import dictConfig
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent.parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logger():
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "[{asctime}] {levelname}: {name}: {message}",
                    "style": "{",
                },
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
                },
            },
            "handlers": {
                "app": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(LOG_DIR / "app.log"),
                    "maxBytes": 5 * 1024 * 1024,
                    "backupCount": 5,
                    "formatter": "default",
                    "level": "INFO",
                },
                "errors": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(LOG_DIR / "errors.log"),
                    "maxBytes": 5 * 1024 * 1024,
                    "backupCount": 5,
                    "formatter": "default",
                    "level": "ERROR",
                },
                "access": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(LOG_DIR / "access.log"),
                    "maxBytes": 5 * 1024 * 1024,
                    "backupCount": 5,
                    "formatter": "default",
                    "level": "INFO",
                },
                "auth": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(LOG_DIR / "auth.log"),
                    "maxBytes": 5 * 1024 * 1024,
                    "backupCount": 5,
                    "formatter": "default",
                    "level": "INFO",
                },
                "source": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(LOG_DIR / "source.log"),
                    "maxBytes": 5 * 1024 * 1024,
                    "backupCount": 5,
                    "formatter": "default",
                    "level": "INFO",
                },
            },
            "loggers": {
                "app_log": {"handlers": ["app"], "level": "DEBUG", "propagate": False},
                "access_log": {
                    "handlers": ["access"],
                    "level": "INFO",
                    "propagate": False,
                },
                "auth_log": {"handlers": ["auth"], "level": "INFO", "propagate": False},
                "source_log": {
                    "handlers": ["source"],
                    "level": "INFO",
                    "propagate": False,
                },
                "errors_log": {
                    "handlers": ["errors"],
                    "level": "DEBUG",
                    "propagate": False,
                },
            },
        }
    )
