from collections.abc import AsyncGenerator
from contextlib import contextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from src.shared.db.engine import async_engine, sync_engine

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


@contextmanager
def get_sync_session():
    """Контекстный менеджер для синхронной сессии."""
    SessionLocal = sessionmaker(bind=sync_engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
