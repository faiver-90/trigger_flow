from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from src.modules.auth.api.v1.auth_router import v1_auth
from src.modules.auth.api.v1.services.auth_service import AuthService
from src.modules.auth.configs.crypt_conf import pwd_context
from src.modules.auth.exceptions_handle.stream_exceptions_handlers import (
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from src.modules.auth.repositories.jwt_repo import JWTRepo
from src.modules.auth.repositories.user_repo import UserRepository
from src.shared.db.models.auth import User
from src.shared.deps.auth_dependencies import authenticate_user, verify_superuser
from src.shared.services.redis_service import RedisService


@pytest.fixture(scope="function")
def test_app():
    app = FastAPI()

    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore
    app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore
    app.add_exception_handler(Exception, generic_exception_handler)

    @app.get("/validation-error")
    async def validation_route(limit: int):
        return {"limit": limit}

    @app.get("/http-error")
    async def http_error_route():
        raise HTTPException(status_code=403, detail="Forbidden action")

    @app.get("/unexpected-error")
    async def unexpected_route():
        raise RuntimeError("Something went wrong")

    @app.get("/")
    async def root():
        return {"It's": "Work"}

    @app.get("/auth-only")
    async def auth_only_route(user=Depends(authenticate_user)):
        return {"user": user}

    @app.get("/superuser-only")
    async def superuser_only_route(user=Depends(verify_superuser)):
        return {"user": user}

    return app


@pytest.fixture(scope="function")
def sync_client(test_app):
    return TestClient(test_app, raise_server_exceptions=False)


@pytest.fixture(scope="function")
async def async_client(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
def mock_result():
    return MagicMock()


@pytest.fixture(scope="function")
def async_mock_session():
    session = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="function")
def mock_user_repo():
    repo = MagicMock(spec=UserRepository)
    repo.get_by_fields = AsyncMock()
    repo.exists_by_fields = AsyncMock()
    repo.create = AsyncMock()
    repo.list = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture(scope="function")
def mock_jwt_repo():
    repo = MagicMock(spec=JWTRepo)
    repo.create = AsyncMock()
    return repo


@pytest.fixture(scope="function")
def mock_redis_service():
    service = MagicMock(spec=RedisService)
    service.set = AsyncMock()
    service.get = AsyncMock()
    service.delete = AsyncMock()
    service.exists = AsyncMock()
    return service


@pytest.fixture(scope="function")
def auth_service(mock_user_repo, mock_jwt_repo, mock_redis_service):
    return AuthService(
        user_repo=mock_user_repo,
        jwt_repo=mock_jwt_repo,
        redis_service=mock_redis_service,
    )


@pytest.fixture(scope="function")
def mock_user():
    hashed_password = pwd_context.hash("correctpassword")
    user = SimpleNamespace(
        id=1,
        username="testuser",
        email="user@test.com",
        hashed_password=hashed_password,
        is_superuser=False,
    )
    return user


@pytest.fixture(scope="function")
def user_repo(async_mock_session):
    return UserRepository(session=async_mock_session)


@pytest.fixture(scope="function")
def fake_user():
    return User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password=pwd_context.hash("plaintext"),
    )


@pytest.fixture(scope="function")
def auth_api_client():
    app = FastAPI()
    app.include_router(v1_auth)

    service = AsyncMock(spec=AuthService)

    from src.modules.auth.api.v1.deps.get_auth_service import get_auth_service

    async def _override():
        return service

    app.dependency_overrides[get_auth_service] = _override

    client = TestClient(app, raise_server_exceptions=False)
    try:
        yield client, service
    finally:
        app.dependency_overrides.clear()
