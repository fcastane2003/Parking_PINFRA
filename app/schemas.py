"""
app/schemas.py

Responsabilidad:
- Modelos Pydantic para validación de entrada y salida en la API.
"""

from typing import Optional

from pydantic import BaseModel, Field


class EmployeeCreate(BaseModel):
    badge: str = Field(..., min_length=1, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=200)
    department: Optional[str] = None
    position: Optional[str] = None
    is_director: Optional[bool] = False


class VehicleCreate(BaseModel):
    owner_id: int
    plate: str
    type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None


class BoletaCreate(BaseModel):
    plate: str
    basement: Optional[str] = None
    spot_code: Optional[str] = None
    reason: str
    observations: Optional[str] = None


class OperationResponse(BaseModel):
    mensaje: str
