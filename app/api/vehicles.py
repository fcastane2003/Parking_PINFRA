"""
app/api/vehicles.py

Responsabilidad:
- Endpoints para crear y buscar vehículos.
- Usa dependencias get_db y schemas para validación.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import crud
from app.schemas import VehicleCreate

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_vehicle_endpoint(payload: VehicleCreate, db: Session = Depends(get_db)):
    # verificar empleado existe
    emp = crud.get_employee(db, payload.owner_id)
    if emp is None:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado.")

    try:
        veh = crud.create_vehicle(
            db=db,
            owner_id=payload.owner_id,
            plate=payload.plate,
            type=payload.type,
            brand=payload.brand,
            model=payload.model,
            color=payload.color,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        # si IntegrityError de unicidad
        if "UNIQUE" in str(e).upper():
            raise HTTPException(
                status_code=409, detail="La placa ya está registrada."
            ) from e

        raise HTTPException(
            status_code=500, detail="No fue posible crear el vehículo."
        ) from e

    return {
        "mensaje": "Vehículo creado correctamente.",
        "id_vehiculo": veh.id,
        "placa": veh.plate,
    }


@router.get("/plate/{plate}")
def get_vehicle_by_plate(plate: str, db: Session = Depends(get_db)):
    from app.db.utils import normalize_plate

    try:
        plate_norm = normalize_plate(plate)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    # Consulta para obtener vehículo con datos del empleado
    veh = db.execute(
        """
        SELECT v.id, v.plate, v.brand, v.model, v.color,
               v.owner_id, e.full_name, e.badge
        FROM vehicles v
        LEFT JOIN employees e ON v.owner_id = e.id
        WHERE v.plate_normalized = :p
        """,
        {"p": plate_norm},
    ).fetchone()

    if not veh:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado.")

    result = dict(veh)
    return result
