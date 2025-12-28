import logging

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Сформировать ответ для ошибок валидации запросов (HTTP 422)."""
    logger.warning(f"[422] Validation error on {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "code": 422,
            "message": "Validation failed",
            "errors": exc.errors(),
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Преобразовать `HTTPException` в унифицированный JSON-ответ."""
    logger.warning(f"[{exc.status_code}] HTTPException on {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "code": exc.status_code,
            "message": exc.detail,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Обработать непредвиденные ошибки и вернуть ответ 500."""
    logger.exception(f"[500] Unhandled exception on {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "code": 500,
            "message": f"Internal server error {exc}",
        },
    )
