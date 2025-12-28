from passlib.context import CryptContext

from src.shared.configs.get_settings import get_settings

settings = get_settings()
pwd_context = CryptContext(
    schemes=[settings.pwd_context_schemes], deprecated=settings.pwd_context_deprecated
)
