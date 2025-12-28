from datetime import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from src.modules.auth.api.v1.schemas import LoginResponseSchema, UserCreateSchema
from src.modules.auth.api.v1.services.auth_service import AuthService
from src.modules.auth.configs.crypt_conf import pwd_context
from src.shared.configs.get_settings import get_settings

settings = get_settings()


@pytest.mark.anyio
async def test_login_success(
    auth_service,
    mock_user_repo,
    mock_jwt_repo,
    mock_redis_service,
    monkeypatch,
):
    user = SimpleNamespace(
        id=7,
        username="demo",
        email="demo@example.com",
        hashed_password=pwd_context.hash("correct"),
        is_superuser=True,
    )
    mock_user_repo.get_by_fields.return_value = user
    mock_jwt_repo.create.return_value = SimpleNamespace(expires_at=datetime.utcnow())

    access_token = "access-token"
    refresh_token = "refresh-token"

    async def fake_set(uid, token, ttl):  # noqa: ANN001
        assert uid == "7"
        assert token == access_token
        assert ttl == settings.access_expire_seconds

    mock_redis_service.set = AsyncMock(side_effect=fake_set)

    monkeypatch.setattr(
        "src.modules.auth.api.v1.services.auth_service.create_access_token",
        lambda *args, **kwargs: access_token,
    )
    monkeypatch.setattr(
        "src.modules.auth.api.v1.services.auth_service.create_refresh_token",
        lambda *args, **kwargs: refresh_token,
    )

    result = await auth_service.login("demo", "correct")

    assert isinstance(result, LoginResponseSchema)
    assert result.user.username == "demo"
    assert result.user.is_superuser is True
    assert result.access_token == access_token
    assert result.refresh_token == refresh_token
    mock_user_repo.get_by_fields.assert_awaited_once_with(username="demo")
    mock_jwt_repo.create.assert_awaited_once()
    mock_redis_service.set.assert_awaited()


@pytest.mark.anyio
async def test_login_wrong_password(auth_service, mock_user_repo):
    user = SimpleNamespace(
        id=1,
        username="demo",
        email="demo@example.com",
        hashed_password=pwd_context.hash("password"),
        is_superuser=False,
    )
    mock_user_repo.get_by_fields.return_value = user

    with pytest.raises(ValueError, match="Invalid username or password"):
        await auth_service.login("demo", "wrong")


@pytest.mark.anyio
async def test_login_user_not_found(auth_service, mock_user_repo):
    mock_user_repo.get_by_fields.return_value = None

    with pytest.raises(ValueError, match="Invalid username or password"):
        await auth_service.login("missing", "whatever")


@pytest.mark.anyio
async def test_login_requires_user_repo(mock_jwt_repo, mock_redis_service):
    service = AuthService(
        user_repo=None, jwt_repo=mock_jwt_repo, redis_service=mock_redis_service
    )

    with pytest.raises(RuntimeError, match="UserRepository is not initialized"):
        await service.login("demo", "pass")


@pytest.mark.anyio
async def test_login_requires_redis_service(mock_user_repo, mock_jwt_repo, mock_user):
    service = AuthService(
        user_repo=mock_user_repo, jwt_repo=mock_jwt_repo, redis_service=None
    )
    mock_user_repo.get_by_fields.return_value = mock_user

    with pytest.raises(RuntimeError, match="RedisService is not initialized"):
        await service.login("testuser", "correctpassword")


@pytest.mark.anyio
async def test_login_requires_jwt_repo(
    mock_user_repo, mock_redis_service, mock_user, monkeypatch
):
    service = AuthService(
        user_repo=mock_user_repo, jwt_repo=None, redis_service=mock_redis_service
    )
    mock_user_repo.get_by_fields.return_value = mock_user

    monkeypatch.setattr(
        "src.modules.auth.api.v1.services.auth_service.create_access_token",
        lambda *args, **kwargs: "access-token",
    )
    monkeypatch.setattr(
        "src.modules.auth.api.v1.services.auth_service.create_refresh_token",
        lambda *args, **kwargs: "refresh-token",
    )

    with pytest.raises(RuntimeError, match="JWTRepo is not initialized"):
        await service.login("testuser", "correctpassword")

    mock_redis_service.set.assert_awaited_once()


@pytest.mark.anyio
async def test_register_user_success(auth_service, mock_user_repo):
    mock_user_repo.exists_by_fields.return_value = False
    created_user = SimpleNamespace(id=1, username="test", email="mail@test.com")
    mock_user_repo.create.return_value = created_user

    schema = UserCreateSchema(
        username="test", email="mail@test.com", password="plainpw"
    )

    result = await auth_service.register_user(schema)

    assert result is created_user
    mock_user_repo.exists_by_fields.assert_awaited_once_with(
        email="mail@test.com", username="test"
    )
    assert mock_user_repo.create.await_count == 1
    args, kwargs = mock_user_repo.create.await_args
    user_payload, hashed_password = args
    assert user_payload["username"] == "test"
    assert user_payload["email"] == "mail@test.com"
    assert user_payload.get("is_superuser") is False
    assert pwd_context.verify("plainpw", hashed_password)
    assert not kwargs


@pytest.mark.anyio
async def test_register_user_already_exists(auth_service, mock_user_repo):
    mock_user_repo.exists_by_fields.return_value = True

    schema = UserCreateSchema(
        username="test", email="mail@test.com", password="plainpw"
    )

    with pytest.raises(
        ValueError, match="User with this email or username already exists"
    ):
        await auth_service.register_user(schema)

    mock_user_repo.create.assert_not_awaited()


@pytest.mark.anyio
async def test_register_requires_user_repo(mock_jwt_repo, mock_redis_service):
    service = AuthService(
        user_repo=None, jwt_repo=mock_jwt_repo, redis_service=mock_redis_service
    )
    schema = UserCreateSchema(username="demo", email="demo@test.com", password="passpw")

    with pytest.raises(RuntimeError, match="UserRepository is not initialized"):
        await service.register_user(schema)
