import httpx
from fastapi import HTTPException


async def send_request(
    method: str,
    url: str,
    *,
    json=None,
    params=None,
    headers=None,
    timeout=5.0,
    **kwargs,
):
    """
    Отправить HTTP-запрос и обернуть ошибки в `HTTPException`.

    Args:
        method (str): HTTP-метод.
        url (str): Адрес запроса.
        json: Тело запроса в формате JSON.
        params: Query-параметры.
        headers: Пользовательские заголовки.
        timeout (float): Таймаут ожидания ответа.
        **kwargs: Дополнительные параметры клиента `httpx`.

    Returns:
        httpx.Response: Ответ удалённого сервиса.

    Raises:
        HTTPException: При сетевых проблемах или ошибочном статусе.
    """
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(
                method=method,
                url=url,
                json=json,
                params=params,
                headers=headers,
                **kwargs,
            )

        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response

    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Service unreachable: {e}") from e
