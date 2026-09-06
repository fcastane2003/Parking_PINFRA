"""
app/parking/routes.py

Responsabilidad:
- Endpoints para gestionar espacios de estacionamiento.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import ParkingSpot
from app.parking import schemas

router = APIRouter(prefix="/api/parking", tags=["parking"])


@router.get("/spots", response_model=list[schemas.ParkingSpotSchema])
def get_spots(db: Session = Depends(get_db)):
    """Listar todos los espacios de estacionamiento"""
    return db.query(ParkingSpot).order_by(ParkingSpot.id).all()


@router.post(
    "/spots",
    response_model=schemas.ParkingSpotSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_spot(
    spot: schemas.ParkingSpotCreate, db: Session = Depends(get_db)
):
    """Crear un nuevo espacio de estacionamiento"""
    existing = (
        db.query(ParkingSpot).filter(ParkingSpot.slot == spot.slot).first()
    )
    if existing:
        raise HTTPException(
            status_code=400, detail=f"El espacio {spot.slot} ya existe"
        )
    new_spot = ParkingSpot(slot=spot.slot)
    db.add(new_spot)
    db.commit()
    db.refresh(new_spot)
    return new_spot


@router.post(
    "/spots/{spot_id}/occupy", response_model=schemas.ParkingSpotSchema
)
def occupy_spot(spot_id: int, db: Session = Depends(get_db)):
    """Ocupar un espacio de estacionamiento"""
    spot = db.get(ParkingSpot, spot_id)
    if not spot:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    if spot.occupied:
        raise HTTPException(
            status_code=400, detail="El espacio ya está ocupado"
        )
    spot.occupied = True
    db.commit()
    db.refresh(spot)
    return spot


@router.post("/spots/{spot_id}/free", response_model=schemas.ParkingSpotSchema)
def free_spot(spot_id: int, db: Session = Depends(get_db)):
    """Liberar un espacio de estacionamiento"""
    spot = db.get(ParkingSpot, spot_id)
    if not spot:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    if not spot.occupied:
        raise HTTPException(status_code=400, detail="El espacio ya está libre")
    spot.occupied = False
    db.commit()
    db.refresh(spot)
    return spot


@router.delete("/spots/{spot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_spot(spot_id: int, db: Session = Depends(get_db)):
    """Eliminar un espacio de estacionamiento"""
    spot = db.get(ParkingSpot, spot_id)
    if not spot:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    db.delete(spot)
    db.commit()
