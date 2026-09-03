"""app/dependencies.py

Responsabilidad:
- Dependencias para FastAPI que validan token Bearer, recuperan usuario desde BD
  y aplican control por roles.
"""

from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.auth import decodificar_token
from app.auth.auth_db import obtener_usuario_por_username
from app.db.session import get_db
from sqlalchemy.orm import Session

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales requeridas.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Esquema Bearer requerido.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = decodificar_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = payload.get("username") or payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token sin identidad válida.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = obtener_usuario_por_username(db, username)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no existe.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not usuario.get("activo", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado.",
        )

    return usuario


async def get_current_active_user(current_user=Depends(get_current_user)):
    return current_user


def require_roles(roles_permitidos: list[str]) -> Callable:
    if not isinstance(roles_permitidos, list) or not roles_permitidos:
        raise ValueError("roles_permitidos debe ser una lista no vacía.")
    roles_norm = {str(r).strip().lower() for r in roles_permitidos}

    async def checker(current_user = Depends(get_current_user)):
        rol_actual = current_user.get("rol") or current_user.get("role")
        if rol_actual is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario sin rol válido.")
        if str(rol_actual).strip().lower() not in roles_norm:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permisos suficientes.")
        return current_user

    return checker
