import pytest
from fastapi import status

from src.modules.auth.api.v1.schemas import LoginResponseSchema, UserOutSchema


def test_login_endpoint_success(auth_api_client):
    client, service = auth_api_client

    service.login.return_value = LoginResponseSchema(
        access_token="access",
        refresh_token="refresh",
        token_type="bearer",
        expires_at="2030-01-01T00:00:00",
        user=UserOutSchema(
            id=1,
            username="demo",
            email="demo@example.com",
            is_superuser=False,
        ),
    )

    payload = {"username": "demo", "password": "secret"}
    response = client.post("/auth/login", json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["access_token"] == "access"
    service.login.assert_awaited_once()


def test_login_endpoint_failure(auth_api_client):
    client, service = auth_api_client
    service.login.side_effect = ValueError("boom")

    response = client.post("/auth/login", json={"username": "demo", "password": "x"})

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["detail"] == "boom"


def test_register_endpoint_success(auth_api_client):
    client, service = auth_api_client
    service.register_user.return_value = UserOutSchema(
        id=10,
        username="new",
        email="new@example.com",
        is_superuser=False,
    )

    payload = {
        "username": "new",
        "email": "new@example.com",
        "password": "secret",
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "new"
    service.register_user.assert_awaited_once()


def test_register_endpoint_failure(auth_api_client):
    client, service = auth_api_client
    service.register_user.side_effect = RuntimeError("db down")

    payload = {
        "username": "new",
        "email": "new@example.com",
        "password": "secret",
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["detail"] == "db down"


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"username": "only"},
    ],
)
def test_register_endpoint_validation_error(auth_api_client, payload):
    client, _ = auth_api_client

    response = client.post("/auth/register", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
