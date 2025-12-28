from __future__ import annotations

from passlib.context import CryptContext
from pydantic import Field, computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _build_asyncpg_url(
    user: str,
    password: str,
    host: str = "localhost",
    port: int = 5432,
    db: str = "pgres",
) -> str:
    """Собирает asyncpg DSN, если DATABASE_URL не задан явно."""
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"


def _build_psycopg2_url(
    user: str,
    password: str,
    host: str = "localhost",
    port: int = 5432,
    db: str = "pgres",
) -> str:
    """Собирает sync DSN, если SYNC_DATABASE_URL не задан явно."""
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


class Settings(BaseSettings):
    """
    Единая типизированная конфигурация приложения.
    Значения берутся из .env, при отсутствии — используются дефолты ниже.
    """

    debug_db: bool = Field(False, alias="DEBUG_DB")

    # === Security / JWT / Crypto ===
    secret_key: str = Field("secret", alias="SECRET_KEY")
    algorithm: str = Field("HS256", alias="ALGORITHM")

    # TTL-ы приходят как int
    access_expire_min: int = Field(15, alias="ACCESS_EXPIRE_MIN")
    refresh_expire_days: int = Field(7, alias="REFRESH_EXPIRE_DAYS")

    # Passlib (pwd_context)
    pwd_context_schemes: str = Field("bcrypt", alias="PWD_CONTEXT_SCHEMES")
    pwd_context_deprecated: str = Field("auto", alias="PWD_CONTEXT_DEPRECATED")

    # Fernet (симметричное шифрование)
    fernet_key: str | None = Field(None, alias="FERNET_KEY")

    # === SMTP / Email ===
    smtp_host: str | None = Field("smtp.gmail.com", alias="SMTP_HOST")
    smtp_port: int = Field(587, alias="SMTP_PORT")
    smtp_username: str | None = Field(None, alias="SMTP_USERNAME")
    smtp_password: str | None = Field(None, alias="SMTP_PASSWORD")
    from_email: str | None = Field(None, alias="FROM_EMAIL")

    # === Databases (части + готовые DSN) ===
    postgres_user: str = Field("pgres", alias="POSTGRES_USER")
    postgres_password: str = Field("pgres", alias="POSTGRES_PASSWORD")
    postgres_db: str = Field("pgres", alias="POSTGRES_DB")
    postgres_host: str = Field("db", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")

    # Если явно заданы — используем их; иначе соберём из частей выше
    database_url: str | None = Field(None, alias="DATABASE_URL")
    sync_database_url: str | None = Field(None, alias="SYNC_DATABASE_URL")

    # === Redis ===
    redis_password: str | None = Field(None, alias="REDIS_PASSWORD")
    default_redis_url: str = Field(
        "redis://localhost:6379/0", alias="DEFAULT_REDIS_URL"
    )
    redis_url_env: str = Field("redis://localhost:6379/0", alias="REDIS_URL_ENV")
    celery_broker_url: str = Field(
        "redis://localhost:6379/0", alias="CELERY_BROKER_URL"
    )
    celery_result_backend: str = Field(
        "redis://localhost:6379/1", alias="CELERY_RESULT_BACKEND"
    )

    # === External APIs ===
    api_key_openweathermap: str | None = Field(None, alias="API_KEY_OPENWEATHERMAP")
    mailerlite_api_key: str | None = Field(None, alias="MAILERLITE_API_KEY")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ---- Пост-обработка значений ----

    @model_validator(mode="after")
    def _fill_derived_values(self) -> Settings:
        # FROM_EMAIL по умолчанию = SMTP_USERNAME, если не задан
        if not self.from_email and self.smtp_username:
            self.from_email = self.smtp_username

        # DATABASE_URL / SYNC_DATABASE_URL — собираем, если не заданы
        if not self.database_url:
            self.database_url = _build_asyncpg_url(
                self.postgres_user,
                self.postgres_password,
                self.postgres_host,
                self.postgres_port,
                self.postgres_db,
            )
        if not self.sync_database_url:
            self.sync_database_url = _build_psycopg2_url(
                self.postgres_user,
                self.postgres_password,
                self.postgres_host,
                self.postgres_port,
                self.postgres_db,
            )
        return self

    # ---- Удобные производные поля/объекты ----

    @computed_field  # type: ignore[misc]
    @property
    def access_expire_seconds(self) -> int:
        """TTL access-токена в секундах."""
        return int(self.access_expire_min) * 60

    @computed_field  # type: ignore[misc]
    @property
    def refresh_expire_seconds(self) -> int:
        """TTL refresh-токена в секундах (грубо: дни → секунды)."""
        return int(self.refresh_expire_days) * 24 * 60 * 60

    @computed_field  # type: ignore[misc]
    @property
    def pwd_context(self) -> CryptContext:
        """
        Готовый Passlib CryptContext, собранный из настроек.
        Пример: schemes="bcrypt", deprecated="auto".
        """
        # допускаем перечисление через запятую (например, "bcrypt,argon2")
        schemes = [s.strip() for s in self.pwd_context_schemes.split(",") if s.strip()]
        return CryptContext(schemes=schemes, deprecated=self.pwd_context_deprecated)


settings: Settings = Settings()  # type: ignore[call-arg]
