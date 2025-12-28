from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi import HTTPException

from src.modules.auth.api.v1.utils import send_request


@pytest.mark.anyio
async def test_send_request_success():
    mock_response = httpx.Response(status_code=200, json={"ok": True})

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response

        response = await send_request("GET", "https://test.local/api")

        assert response.status_code == 200
        mock_request.assert_called_once_with(
            method="GET",
            url="https://test.local/api",
            json=None,
            params=None,
            headers=None,
        )


@pytest.mark.anyio
async def test_send_request_error_status():
    mock_response = httpx.Response(status_code=404, text="Not found")

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response

        with pytest.raises(HTTPException) as exc:
            await send_request("GET", "https://test.local/not-found")

        assert exc.value.status_code == 404
        assert "Not found" in exc.value.detail


@pytest.mark.anyio
async def test_send_request_request_exception():
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = httpx.ConnectTimeout("Timeout!")

        with pytest.raises(HTTPException) as exc:
            await send_request("GET", "https://test.local/timeout")

        assert exc.value.status_code == 502
        assert "Service unreachable" in exc.value.detail
