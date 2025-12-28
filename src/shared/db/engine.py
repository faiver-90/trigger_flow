from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from src.shared.configs.get_settings import get_settings

settings = get_settings()
# --- Асинхронный движок (для FastAPI) ---
async_engine = create_async_engine(
    settings.database_url,  #  type: ignore[misc]
    echo=settings.debug_db if hasattr(settings, "debug") else False,
    future=True,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)

# --- Синхронный движок (для Alembic, скриптов, Celery и т.д.) ---
sync_engine = create_engine(
    settings.sync_database_url,  #  type: ignore[misc]
    echo=settings.debug_db if hasattr(settings, "debug") else False,
)
