"""
app/db/session.py

Responsabilidad:
- Crear el engine SQLAlchemy a partir de la configuración.
- Exponer SessionLocal y una dependencia get_db para usar en endpoints.
- Soportar SQLite (check_same_thread) y Postgres a través de DATABASE_URL.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings

# Configuración del engine según la URL
DATABASE_URL = settings.DATABASE_URL

engine_kwargs = {}

# Para SQLite local (archivo), necesitamos check_same_thread=False
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        future=True,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        future=True,
    )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
    future=True,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia de FastAPI: yield una sesión y la cierra al final.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
