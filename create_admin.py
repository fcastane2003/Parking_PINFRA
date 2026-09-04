from getpass import getpass
from app.db.session import SessionLocal
from app.auth.auth import hash_password
from app.db.models import User
from app.config import settings

# Intentamos leer usuario/contraseña desde settings (.env)
USERNAME = getattr(settings, "INITIAL_ADMIN_USERNAME", "admin")
PASSWORD = getattr(settings, "INITIAL_ADMIN_PASSWORD", None)

# Si no hay contraseña en settings, la solicitamos en la terminal (oculta)
if not PASSWORD:
    PASSWORD = getpass(
        "Escribe la contraseña para el usuario admin (no se mostrará): "
    ).strip()
    if not PASSWORD:
        print("No se proporcionó contraseña. Abortando.")
        raise SystemExit(1)

db = SessionLocal()
try:
    u = db.query(User).filter_by(username=USERNAME).first()
    if u:
        print("Admin ya existe — actualizando contraseña y campos básicos.")
        u.hashed_password = hash_password(PASSWORD)
        u.email = u.email or "admin@example.com"
        u.full_name = u.full_name or "Administrador"
        u.role = "admin"
        u.active = True
        db.add(u)
        db.commit()
        print(f"Admin actualizado (id={u.id}).")
    else:
        print("Creando usuario admin.")
        admin = User(
            username=USERNAME,
            email="admin@example.com",
            hashed_password=hash_password(PASSWORD),
            full_name="Administrador",
            role="admin",
            active=True,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(f"Admin creado (id={admin.id}).")
finally:
    db.close()
