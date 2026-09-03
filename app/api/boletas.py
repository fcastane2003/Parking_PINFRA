"""
app/api/boletas.py

Responsabilidad:
- Endpoint para crear una boleta administrativa (genera folio).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import BoletaCreate
from app.db.utils import normalize_plate
from app.services.folio import create_boleta_with_folio

router = APIRouter(prefix="/api/boletas", tags=["boletas"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_boleta(payload: BoletaCreate, db: Session = Depends(get_db)):
    try:
        plate_norm = normalize_plate(payload.plate)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    try:
        boleta = create_boleta_with_folio(
            db=db,
            plate=payload.plate,
            plate_normalized=plate_norm,
            reason=payload.reason,
            observations=payload.observations,
            employee_id=None,
            vehicle_id=None,
            basement=payload.basement,
            spot_code=payload.spot_code,
            created_by=None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="No fue posible crear la boleta.") from e

    return {
        "mensaje": "Boleta creada correctamente.",
        "folio": boleta.folio,
        "id_boleta": boleta.id,
    }
