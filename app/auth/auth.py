"""app/auth/auth.py

Responsabilidad:
- Hash y verificación de contraseñas (bcrypt).
- Creación y decodificación de tokens JWT (python-jose).
- Valores de expiración obtenidos desde app.config.settings.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import bcrypt
from jose import JWTError, jwt

from app.config import settings


def _normalizar_password(password: str) -> bytes:
    if not isinstance(password, str):
        raise TypeError("La contraseña debe ser texto.")
    if not password:
        raise ValueError("La contraseña no puede estar vacía.")
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        raise ValueError("La contraseña supera el límite de 72 bytes de bcrypt.")
    return password_bytes


def hash_password(password: str) -> str:
    pw = _normalizar_password(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw, salt)
    return hashed.decode("utf-8")


def verificar_password(plain_password: str, hashed_password: str) -> bool:
    try:
        pw = _normalizar_password(plain_password)
        if not isinstance(hashed_password, str):
            return False
        return bcrypt.checkpw(pw, hashed_password.encode("utf-8"))
    except Exception:
        return False


def crear_token_acceso(
    data: dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    if not isinstance(data, dict):
        raise TypeError("data debe ser dict.")
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire, "sub": data.get("sub")})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decodificar_token(token: str) -> Optional[dict[str, Any]]:
    if not isinstance(token, str) or not token.strip():
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        rol = payload.get("rol")
        if not isinstance(username, str):
            return None
        return {"username": username, "rol": rol}
    except JWTError:
        return None
