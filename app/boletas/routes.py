"""
app/boletas/routes.py

Responsabilidad:
- Endpoints para gestionar boletas.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.boletas import services, schemas

router = APIRouter(prefix="/api/boletas", tags=["boletas"])


@router.post(
    "/",
    response_model=schemas.BoletaSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_boleta_endpoint(
    boleta: schemas.BoletaCreate, db: Session = Depends(get_db)
):
    """Crear una nueva boleta (registro de entrada)"""
    try:
        result = services.create_boleta(
            db=db,
            plate=boleta.plate,
            vehicle_id=boleta.vehicle_id,
            employee_id=boleta.employee_id,
            basement=boleta.basement,
            spot_code=boleta.spot_code,
            reason=boleta.reason,
            observations=boleta.observations,
            created_by=1,  # Usuario admin por defecto
        )
        if not result:
            raise HTTPException(
                status_code=400, detail="No se pudo crear la boleta"
            )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{boleta_id}/close", response_model=schemas.BoletaSchema)
def close_boleta_endpoint(boleta_id: int, db: Session = Depends(get_db)):
    """Cerrar una boleta (registro de salida)"""
    result = services.close_boleta(db, boleta_id)
    if not result:
        raise HTTPException(status_code=404, detail="Boleta no encontrada")
    return result


@router.get("/", response_model=List[schemas.BoletaSchema])
def list_boletas_endpoint(
    active_only: bool = False, db: Session = Depends(get_db)
):
    """Listar boletas"""
    return services.list_boletas(db, active_only)


@router.get("/{boleta_id}", response_model=schemas.BoletaSchema)
def get_boleta_endpoint(boleta_id: int, db: Session = Depends(get_db)):
    """Obtener una boleta por ID"""
    boleta = services.get_boleta(db, boleta_id)
    if not boleta:
        raise HTTPException(status_code=404, detail="Boleta no encontrada")
    return boleta
