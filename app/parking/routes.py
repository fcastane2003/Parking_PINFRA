from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.parking import services, schemas

router = APIRouter(prefix="/api/parking", tags=["parking"])


@router.get("/spots", response_model=list[schemas.ParkingSpotSchema])
def get_spots(db: Session = Depends(get_db)):
    """List all parking spots"""
    return services.list_spots(db)
