from datetime import datetime, timedelta

import pytest
from jose import JWTError, jwt

from src.modules.auth.api.v1.schemas import JWTCreateSchema
from src.modules.auth.repositories.jwt_repo import JWTRepo
from src.shared.configs.get_settings import get_settings
from src.shared.services.jwt_service import (
    create_access_token,
    create_refresh_token,
    create_token,
    decode_token,
)

settings = get_settings()


@pytest.mark.anyio
async def test_jwt_repo_create_persists_token(async_mock_session):
    repo = JWTRepo(session=async_mock_session)
    schema = JWTCreateSchema(user_id=1, token="mock_token")

    result = await repo.create(schema)

    async_mock_session.add.assert_called_once_with(result)
    async_mock_session.commit.assert_awaited_once()
    async_mock_session.refresh.assert_awaited_once_with(result)
    assert result.user_id == 1
    assert result.token == "mock_token"
    assert result.expires_at.tzinfo is None


def test_create_token_contains_exp_and_sub(monkeypatch):
    monkeypatch.setattr(settings, "secret_key", "unit-secret")
    monkeypatch.setattr(settings, "algorithm", "HS256")
    fixed_now = datetime(2030, 1, 1, 0, 0, 0)

    class FrozenDateTime(datetime):
        @classmethod
        def utcnow(cls):  # noqa: N805
            return fixed_now

    monkeypatch.setattr("src.shared.services.jwt_service.datetime", FrozenDateTime)

    token = create_token({"sub": "123"}, timedelta(minutes=5))
    decoded = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

    assert decoded["sub"] == "123"
    expires_at = datetime.utcfromtimestamp(decoded["exp"])
    assert expires_at == fixed_now + timedelta(minutes=5)


def test_create_access_token_uses_access_settings(monkeypatch):
    monkeypatch.setattr(settings, "secret_key", "unit-secret")
    monkeypatch.setattr(settings, "algorithm", "HS256")
    monkeypatch.setattr(settings, "access_expire_min", 1)

    token = create_access_token("42", is_superuser=True)
    decoded = decode_token(token)

    assert decoded["sub"] == "42"
    assert decoded["is_superuser"] is True
    expires_at = datetime.utcfromtimestamp(decoded["exp"])
    delta = expires_at - datetime.utcnow()
    assert 30 <= delta.total_seconds() <= 90


def test_create_refresh_token_uses_refresh_settings(monkeypatch):
    monkeypatch.setattr(settings, "secret_key", "unit-secret")
    monkeypatch.setattr(settings, "algorithm", "HS256")
    monkeypatch.setattr(settings, "refresh_expire_days", 2)

    token = create_refresh_token("42")
    decoded = decode_token(token)

    assert decoded["sub"] == "42"
    expires_at = datetime.utcfromtimestamp(decoded["exp"])
    delta_days = (expires_at - datetime.utcnow()).total_seconds() / (24 * 3600)
    assert 1.9 <= delta_days <= 2.1


def test_decode_token_with_invalid_signature(monkeypatch):
    monkeypatch.setattr(settings, "secret_key", "unit-secret")
    monkeypatch.setattr(settings, "algorithm", "HS256")

    token = create_access_token("123")
    broken_token = token + "tamper"

    with pytest.raises(JWTError):
        decode_token(broken_token)


def test_expired_token(monkeypatch):
    monkeypatch.setattr(settings, "secret_key", "unit-secret")
    monkeypatch.setattr(settings, "algorithm", "HS256")

    token = create_token({"sub": "123"}, timedelta(seconds=-1))

    with pytest.raises(JWTError):
        decode_token(token)
