"""app/auth/auth_db.py

Responsabilidad:
- Operaciones sobre usuarios usando SQLAlchemy Session.
- Inicialización del admin inicial desde variables de entorno.
"""

from typing import Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import User
from app.auth.auth import hash_password
from app.config import settings


def init_auth_db(db: Session) -> None:
    """
    Crea el usuario administrador inicial si no existe.
    Debe llamarse una vez en el arranque (dentro de una sesión).
    """
    initial_username = (
        settings.__dict__.get("INITIAL_ADMIN_USERNAME") or ""
    ).strip()
    initial_email = (
        settings.__dict__.get("INITIAL_ADMIN_EMAIL") or ""
    ).strip()
    initial_password = settings.__dict__.get("INITIAL_ADMIN_PASSWORD") or ""

    if not initial_username or not initial_email or not initial_password:
        # No hay administrador por crear
        return

    stmt = select(User).where(User.username == initial_username)
    existing = db.execute(stmt).scalars().first()
    if existing:
        return

    hashed = hash_password(initial_password)
    admin = User(
        username=initial_username,
        email=initial_email,
        hashed_password=hashed,
        full_name="Administrador",
        role="admin",
        active=True,
    )
    db.add(admin)
    db.commit()


def crear_usuario(
    db: Session,
    username: str,
    email: str,
    password: str,
    nombre_completo: str,
    rol: str = "operador",
) -> Optional[int]:
    username = username.strip()
    email = email.strip().lower()
    if not username or not email or not password:
        raise ValueError("username, email y password son requeridos.")

    hashed = hash_password(password)

    usuario = User(
        username=username,
        email=email,
        hashed_password=hashed,
        full_name=nombre_completo,
        role=rol,
        active=True,
    )

    try:
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario.id
    except Exception:
        db.rollback()
        return None


def obtener_usuario_por_username(
    db: Session, username: str
) -> Optional[dict[str, Any]]:
    if not username or not isinstance(username, str):
        return None
    stmt = select(User).where(User.username == username.strip())
    row = db.execute(stmt).scalars().first()
    if row is None:
        return None
    return {
        "id": row.id,
        "username": row.username,
        "email": row.email,
        "hashed_password": row.hashed_password,
        "full_name": row.full_name,
        "rol": row.role,
        "activo": row.active,
    }


def obtener_usuario_por_id(
    db: Session, user_id: int
) -> Optional[dict[str, Any]]:
    if not isinstance(user_id, int) or user_id <= 0:
        return None
    user = db.get(User, user_id)
    if user is None:
        return None
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "hashed_password": user.hashed_password,
        "full_name": user.full_name,
        "rol": user.role,
        "activo": user.active,
    }


def listar_usuarios(db: Session) -> list[dict[str, Any]]:
    stmt = select(User)
    rows = db.execute(stmt).scalars().all()
    result = []
    for r in rows:
        result.append(
            {
                "id": r.id,
                "username": r.username,
                "email": r.email,
                "full_name": r.full_name,
                "role": r.role,
                "active": r.active,
                "created_at": (
                    r.created_at.isoformat()
                    if getattr(r, "created_at", None)
                    else None
                ),
            }
        )
    return result


def actualizar_rol_usuario(db: Session, user_id: int, nuevo_rol: str) -> bool:
    if not isinstance(user_id, int) or user_id <= 0:
        return False
    user = db.get(User, user_id)
    if not user:
        return False
    user.role = nuevo_rol
    db.add(user)
    db.commit()
    return True


def desactivar_usuario(db: Session, user_id: int) -> bool:
    if not isinstance(user_id, int) or user_id <= 0:
        return False
    user = db.get(User, user_id)
    if not user:
        return False
    user.active = False
    db.add(user)
    db.commit()
    return True
