from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError

from src.modules.auth.api.v1.auth_router import v1_auth
from src.modules.auth.exceptions_handle.stream_exceptions_handlers import (
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from src.modules.notifications.api.v1.router import v1_notification_router
from src.modules.source.api.v1.router import v1_api_source
from src.modules.trigger.api.v1.trigger_router import v1_trigger_router
from src.shared.celery_module.celery_worker import celery_app
from src.shared.configs.log_conf import setup_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    print("Логирование инициализировано")
    yield
    print("Приложение останавливается")


def get_app() -> FastAPI:
    app_init = FastAPI(version="1.0.0", docs_url="/swagger", lifespan=lifespan)

    from sqlalchemy import text
    from sqlalchemy.exc import SQLAlchemyError
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.shared.db.session import get_async_session

    @app_init.get(
        "/health_check",
        summary="Проверка работоспособности приложения и базы данных",
        description="Возвращает статус работы сервера и подключения к базе данных.",
        tags=["Service"],
    )
    async def health_check(
        session: AsyncSession = Depends(get_async_session),
    ) -> dict[str, str]:
        try:
            celery_app.send_task("sync_articles")
            await session.execute(text("SELECT 1"))
            return {"status": "ok", "database": "connected"}
        except SQLAlchemyError as e:
            return {"status": "error", "database": f"unavailable: {str(e)}"}
        except Exception as e:
            return {"status": "error", "database": f"unavailable: {str(e)}"}

    app_init.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore
    app_init.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore
    app_init.add_exception_handler(Exception, generic_exception_handler)
    app_init.include_router(v1_auth)
    app_init.include_router(v1_api_source)
    app_init.include_router(v1_notification_router)
    app_init.include_router(v1_trigger_router)

    return app_init


app = get_app()
