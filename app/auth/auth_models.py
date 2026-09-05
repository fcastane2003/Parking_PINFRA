"""app/auth/auth_models.py

Responsabilidad:
- Modelos Pydantic para login, registro y token.
"""

from pydantic import BaseModel
from typing import Optional


class UsuarioCreate(BaseModel):
    username: str
    email: str
    password: str
    nombre_completo: str
    rol: str = "operador"


class UsuarioLogin(BaseModel):
    username: str
    password: str


class UsuarioUpdate(BaseModel):
    rol: Optional[str] = None
    activo: Optional[bool] = None
    nombre_completo: Optional[str] = None
    email: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    username: Optional[str] = None
    rol: Optional[str] = None
