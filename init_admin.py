from app.db.session import SessionLocal
from app.auth.auth_db import init_auth_db

db = SessionLocal()
try:
    init_auth_db(db)
    print("init_auth_db executed")
finally:
    db.close()
