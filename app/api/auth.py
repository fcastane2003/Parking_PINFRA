"""app/api/auth.py

Responsabilidad:
- Endpoints para login, registro y obtener información del usuario actual.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth_models import UsuarioLogin, UsuarioCreate, UsuarioUpdate
from app.auth.auth import verificar_password, crear_token_acceso
from app.auth.auth_db import (
    crear_usuario,
    obtener_usuario_por_username,
    listar_usuarios,
    actualizar_rol_usuario,
    desactivar_usuario,
)
from app.db.session import get_db
from app.dependencies import get_current_active_user, require_roles
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login")
def login(payload: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = obtener_usuario_por_username(db, payload.username)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos.",
        )
    if not verificar_password(payload.password, usuario["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos.",
        )

    if not usuario.get("activo", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado.",
        )

    token_data = {"sub": usuario["username"], "rol": usuario.get("rol")}
    token = crear_token_acceso(token_data)

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "id": usuario["id"],
            "username": usuario["username"],
            "nombre_completo": usuario.get("full_name"),
            "rol": usuario.get("rol"),
        },
    }


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    payload: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(["admin"])),
):
    user_id = crear_usuario(
        db,
        username=payload.username,
        email=payload.email,
        password=payload.password,
        nombre_completo=payload.nombre_completo,
        rol=payload.rol,
    )
    if not user_id:
        raise HTTPException(status_code=400, detail="El usuario o email ya existe.")
    return {"mensaje": "Usuario creado correctamente.", "id": user_id}


@router.get("/usuarios")
def listar(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(["admin"])),
):
    usuarios = listar_usuarios(db)
    return {"usuarios": usuarios}


@router.get("/me")
def me(current_user: dict = Depends(get_current_active_user)):
    return current_user


@router.put("/usuarios/{user_id}")
def actualizar_usuario(
    user_id: int,
    payload: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(["admin"])),
):
    if payload.rol:
        actualizar_rol_usuario(db, user_id, payload.rol)
    if payload.activo is not None and not payload.activo:
        desactivar_usuario(db, user_id)
    return {"mensaje": "Usuario actualizado correctamente."}
