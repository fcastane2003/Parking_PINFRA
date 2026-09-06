"""
app/boletas/schemas.py

Responsabilidad:
- Esquemas Pydantic para boletas.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BoletaSchema(BaseModel):
    id: int
    folio: str
    plate: str
    vehicle_id: Optional[int] = None
    employee_id: Optional[int] = None
    basement: Optional[str] = None
    spot_code: Optional[str] = None
    reason: Optional[str] = None
    observations: Optional[str] = None
    state: str
    created_at: datetime

    class Config:
        orm_mode = True


class BoletaCreate(BaseModel):
    plate: str
    vehicle_id: Optional[int] = None
    employee_id: Optional[int] = None
    basement: Optional[str] = None
    spot_code: Optional[str] = None
    reason: Optional[str] = None
    observations: Optional[str] = None
