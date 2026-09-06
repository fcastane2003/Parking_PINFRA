from sqlalchemy.orm import Session
from app.db.models import ParkingSpot


def list_spots(db: Session):
    return db.query(ParkingSpot).order_by(ParkingSpot.id).all()
