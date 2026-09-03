"""
app/tests/test_vehicles.py

Responsabilidad:
- Test que valida que un empleado no pueda tener más de 3 vehículos.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base
from app.db.crud import create_employee, create_vehicle, count_vehicles_for_employee


@pytest.fixture()
def in_memory_db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, future=True)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, future=True)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_max_three_vehicles(in_memory_db):
    db = in_memory_db

    # Crear empleado
    emp = create_employee(db, badge="EMP001", full_name="Prueba Uno")

    # Crear 3 vehículos OK
    create_vehicle(db, owner_id=emp.id, plate="AAA111")
    create_vehicle(db, owner_id=emp.id, plate="BBB222")
    create_vehicle(db, owner_id=emp.id, plate="CCC333")

    # Cuarto vehículo debe fallar
    with pytest.raises(ValueError):
        create_vehicle(db, owner_id=emp.id, plate="DDD444")

    # Confirmar conteo = 3
    assert count_vehicles_for_employee(db, emp.id) == 3
