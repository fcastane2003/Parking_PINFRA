"""
app/db/models.py

Responsabilidad:
- Contiene las definiciones de modelo SQLAlchemy usadas por la aplicaciÃ³n.
- Mantener el esquema mÃ­nimo necesario para Sprint 0.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    badge = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(200), nullable=False)
    department = Column(String(150))
    position = Column(String(100))
    is_director = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    vehicles = relationship("Vehicle", back_populates="owner")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String(64), nullable=False)
    plate_normalized = Column(String(64), nullable=False, index=True)
    brand = Column(String(100))
    model = Column(String(100))
    color = Column(String(50))
    type = Column(String(50))
    owner_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    is_company = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("Employee", back_populates="vehicles")

    __table_args__ = (
        UniqueConstraint("plate_normalized", name="uq_vehicle_plate_normalized"),
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(254), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200))
    role = Column(String(50), default="operador")
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BoletaCounter(Base):
    __tablename__ = "boleta_counters"

    year = Column(Integer, primary_key=True)
    counter = Column(Integer, nullable=False, default=0)


class Boleta(Base):
    __tablename__ = "boletas"

    id = Column(Integer, primary_key=True)
    folio = Column(String(64), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    plate = Column(String(64), nullable=False)
    plate_normalized = Column(String(64), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    basement = Column(String(20))
    spot_code = Column(String(50))
    reason = Column(String(200))
    observations = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    state = Column(String(32), default="abierta")


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True)
    boleta_id = Column(Integer, ForeignKey("boletas.id", ondelete="CASCADE"))
    filename = Column(String(255))
    content_type = Column(String(128))
    path = Column(String(1024))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ParkingSpot(Base):
    __tablename__ = "parking_spots"
    id = Column(Integer, primary_key=True, index=True)
    slot = Column(String, unique=True, index=True)
    occupied = Column(Boolean, default=False)
