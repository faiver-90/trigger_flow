from functools import lru_cache

from src.shared.configs.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
