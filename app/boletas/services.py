"""
app/boletas/services.py

Responsabilidad:
- Servicios para boletas y registros de entrada/salida.
"""

from sqlalchemy.orm import Session
from app.db.models import Boleta
from app.db.utils import normalize_plate


def create_boleta(
    db: Session,
    plate: str,
    vehicle_id: int = None,
    employee_id: int = None,
    basement: str = None,
    spot_code: str = None,
    reason: str = None,
    observations: str = None,
    created_by: int = None,
):
    """Crear una nueva boleta (entrada)"""
    from app.services.folio import generate_folio_and_create_boleta

    # Normalizar la placa
    plate_normalized = normalize_plate(plate)

    return generate_folio_and_create_boleta(
        db=db,
        plate=plate,
        plate_normalized=plate_normalized,
        vehicle_id=vehicle_id,
        employee_id=employee_id,
        basement=basement,
        spot_code=spot_code,
        reason=reason,
        observations=observations,
        created_by=created_by,
    )


def close_boleta(db: Session, boleta_id: int):
    """Cerrar una boleta (salida)"""
    boleta = db.get(Boleta, boleta_id)
    if not boleta:
        return None
    boleta.state = "cerrada"
    db.commit()
    db.refresh(boleta)
    return boleta


def list_boletas(db: Session, active_only: bool = False):
    """Listar boletas, opcionalmente solo activas"""
    query = db.query(Boleta)
    if active_only:
        query = query.filter(Boleta.state == "abierta")
    return query.order_by(Boleta.created_at.desc()).all()


def get_boleta(db: Session, boleta_id: int):
    """Obtener una boleta por ID"""
    return db.get(Boleta, boleta_id)
