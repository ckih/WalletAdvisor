import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-for-jwt"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str = "postgresql://afa_user:afa_password@localhost:5432/afa_db"

    ENCRYPTION_KEY: str = "default-static-encryption-key-must-be-replaced-in-env"

    ANTHROPIC_API_KEY: str = ""

    KAFKA_BOOTSTRAP_SERVERS: str = ""
    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"

settings = Settings()

class EncryptionService:
    def __init__(self, key: str = settings.ENCRYPTION_KEY):
        self.fernet = Fernet(key.encode())

    def encrypt(self, data: str) -> str:
        if not data:
            return data
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        if not encrypted_data:
            return encrypted_data
        return self.fernet.decrypt(encrypted_data.encode()).decode()

encryption_service = EncryptionService()
