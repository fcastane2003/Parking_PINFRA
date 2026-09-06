"""
Configuración de la aplicación.
"""

from pathlib import Path
from pydantic import BaseSettings
from dotenv import load_dotenv
from typing import List

# Cargar el .env de forma absoluta
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    REDIS_URL: str = ""
    INITIAL_ADMIN_USERNAME: str = "admin"
    INITIAL_ADMIN_EMAIL: str = "admin@example.com"
    INITIAL_ADMIN_PASSWORD: str
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Variables para JWT (agregadas)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 días
    ALGORITHM: str = "HS256"

    class Config:
        env_file = str(BASE_DIR / ".env")
        case_sensitive = True


settings = Settings()
