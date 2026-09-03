"""
Configuración de la aplicación.

Responsabilidad:
- Cargar variables de entorno (.env) mediante pydantic BaseSettings.
- Exponer objeto `settings` usado por el resto de la aplicación.
"""
from pydantic import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str = "sqlite:///./database/empleados.db"
    REDIS_URL: Optional[str] = None
    ALLOWED_ORIGINS: List[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
