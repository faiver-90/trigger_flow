import os

import redis.asyncio as redis
from fastapi import Depends

from src.shared.services.redis_service import RedisService

REDIS_URL_ENV = "REDIS_URL"
DEFAULT_REDIS_URL = "redis://localhost:6379/0"


async def get_redis_client():
    url = os.getenv(REDIS_URL_ENV, DEFAULT_REDIS_URL)
    client = redis.from_url(url, decode_responses=True)
    try:
        yield client
    finally:
        await client.aclose()


async def get_redis_service(
    client: redis.Redis = Depends(get_redis_client),
) -> RedisService:
    return RedisService(client)
