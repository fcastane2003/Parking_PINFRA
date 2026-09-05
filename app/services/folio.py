"""
app/services/folio.py

Responsabilidad:
- Servicio ligero que encapsula la creación de boleta con folio.
- Provee función create_boleta_with_folio(db, boleta_data).
"""

from sqlalchemy.orm import Session

from app.db.crud import generate_folio_and_create_boleta


def create_boleta_with_folio(db: Session, **kwargs):
    """
    Delegar a la función del CRUD que genera el folio y crea la boleta.

    Args:
        db: Sesión de base de datos
        **kwargs: plate, plate_normalized, reason, observations,
                 employee_id, vehicle_id, basement, spot_code, created_by

    Returns:
        Boleta creada con folio generado
    """
    return generate_folio_and_create_boleta(db=db, **kwargs)
