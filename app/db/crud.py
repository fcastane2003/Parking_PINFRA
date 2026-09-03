"""
app/db/crud.py

Responsabilidad:
- Operaciones CRUD atómicas usadas por los endpoints.
- Impone regla de negocio: máximo 3 vehículos por colaborador.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import select, update, insert, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import Employee, Vehicle, Boleta, BoletaCounter
from app.db.utils import normalize_plate


def create_employee(db: Session, badge: str, full_name: str, **kwargs) -> Employee:
    emp = Employee(badge=badge, full_name=full_name, **kwargs)
    db.add(emp)
    try:
        db.commit()
        db.refresh(emp)
        return emp
    except Exception:
        db.rollback()
        raise


def get_employee(db: Session, employee_id: int) -> Optional[Employee]:
    return db.get(Employee, employee_id)


def count_vehicles_for_employee(db: Session, employee_id: int) -> int:
    stmt = select(Vehicle).where(Vehicle.owner_id == employee_id)
    result = db.execute(stmt).scalars().all()
    return len(result)


def create_vehicle(
    db: Session,
    owner_id: int,
    plate: str,
    type: Optional[str] = None,
    brand: Optional[str] = None,
    model: Optional[str] = None,
    color: Optional[str] = None,
) -> Vehicle:
    """
    Crea un vehículo verificando la regla de negocio:
    máximo 3 vehículos por colaborador.

    Hace la operación dentro de una transacción. Para SQLite
    intenta usar BEGIN IMMEDIATE para reducir condiciones de carrera.
    """

    if not isinstance(owner_id, int) or owner_id <= 0:
        raise ValueError("owner_id no es válido.")

    plate_norm = normalize_plate(plate)

    # Intentar asegurar atomicidad extra en SQLite
    if db.bind.dialect.name == "sqlite":
        # BEGIN IMMEDIATE para bloquear la DB y evitar race conditions
        db.execute(text("BEGIN IMMEDIATE"))

    try:
        # contar vehículos actuales
        stmt_count = select(Vehicle).where(Vehicle.owner_id == owner_id)
        current = len(db.execute(stmt_count).scalars().all())
        if current >= 3:
            raise ValueError("El colaborador ya tiene el número máximo de vehículos (3).")

        # verificar unicidad placa normalizada
        stmt_plate = select(Vehicle).where(Vehicle.plate_normalized == plate_norm)
        existing = db.execute(stmt_plate).scalars().first()
        if existing:
            raise IntegrityError("UNIQUE constraint failed: vehicles.plate_normalized", None, None)

        veh = Vehicle(
            plate=plate,
            plate_normalized=plate_norm,
            brand=brand,
            model=model,
            color=color,
            type=type,
            owner_id=owner_id,
        )
        db.add(veh)
        db.commit()
        db.refresh(veh)
        return veh

    except IntegrityError:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise


def generate_folio_and_create_boleta(
    db: Session,
    plate: str,
    plate_normalized: str,
    reason: str,
    observations: Optional[str],
    employee_id: Optional[int],
    vehicle_id: Optional[int],
    basement: Optional[str],
    spot_code: Optional[str],
    created_by: Optional[int],
) -> Boleta:
    """
    Genera folio (incremental por año) y crea la boleta
    dentro de una transacción atómica.
    """
    year = datetime.utcnow().year

    try:
        if db.bind.dialect.name == "sqlite":
            db.execute(text("BEGIN IMMEDIATE"))

        # obtener o crear contador del año
        counter = db.get(BoletaCounter, year)
        if counter is None:
            counter = BoletaCounter(year=year, counter=1)
            db.add(counter)
            db.flush()
            seq = 1
        else:
            counter.counter += 1
            db.add(counter)
            db.flush()
            seq = counter.counter

        mm = datetime.utcnow().strftime("%m")
        folio = f"A-{mm}{year}-{str(seq).zfill(5)}"

        boleta = Boleta(
            folio=folio,
            plate=plate,
            plate_normalized=plate_normalized,
            vehicle_id=vehicle_id,
            employee_id=employee_id,
            basement=basement,
            spot_code=spot_code,
            reason=reason,
            observations=observations,
            created_by=created_by,
            state="abierta",
        )
        db.add(boleta)
        db.commit()
        db.refresh(boleta)
        return boleta

    except Exception:
        db.rollback()
        raise
