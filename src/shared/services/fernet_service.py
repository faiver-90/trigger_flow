from cryptography.fernet import Fernet, InvalidToken

from src.shared.configs.get_settings import get_settings

settings = get_settings()


class FernetService:
    def __init__(self, fernet_key: str = None):  # type: ignore
        """
        :param fernet_key: Ключ в виде строки. Если None, берется из FERNET_KEY.
        """
        key = settings.fernet_key

        if not key:
            raise ValueError(
                "Fernet key not specified (neither in argument nor in FERNET_KEY)"
            )
        self.fernet = Fernet(key.encode())

    def encrypt_str(self, data: str | bytes) -> str:
        """Шифрует строку или байты, возвращает base64-строку."""
        if isinstance(data, str):
            data = data.encode()
        encrypted = self.fernet.encrypt(data)
        return encrypted.decode()

    def decrypt_str(self, encrypted_data: str | bytes) -> str:
        """Расшифровывает данные в исходную строку."""
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        try:
            decrypted = self.fernet.decrypt(encrypted_data)
            return decrypted.decode()
        except InvalidToken as e:
            raise ValueError("Invalid key or corrupted data") from e
