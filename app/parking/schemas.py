"""
app/parking/schemas.py

Responsabilidad:
- Esquemas Pydantic para el módulo de estacionamiento.
"""

from pydantic import BaseModel


class ParkingSpotSchema(BaseModel):
    id: int
    slot: str
    occupied: bool

    class Config:
        orm_mode = True


class ParkingSpotCreate(BaseModel):
    slot: str
