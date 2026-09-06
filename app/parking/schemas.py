from pydantic import BaseModel


class ParkingSpotSchema(BaseModel):
    id: int
    slot: str
    occupied: bool

    class Config:
        orm_mode = True
