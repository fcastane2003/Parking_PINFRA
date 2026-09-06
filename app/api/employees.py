"""app/api/employees.py

Responsabilidad:
- Endpoints CRUD para empleados.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import EmployeeCreate
from app.db.crud import create_employee, get_employee

router = APIRouter(prefix="/api/employees", tags=["employees"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_employee_endpoint(payload: EmployeeCreate, db: Session = Depends(get_db)):
    emp = create_employee(
        db,
        badge=payload.badge,
        full_name=payload.full_name,
        department=payload.department,
        position=payload.position,
        is_director=payload.is_director,
    )
    return {"mensaje": "Empleado creado", "id": emp.id}


@router.get("")
def list_employees(db: Session = Depends(get_db)):
    from sqlalchemy import select
    from app.db.models import Employee

    rows = db.execute(select(Employee)).scalars().all()
    return {
        "employees": [
            {
                "id": r.id,
                "badge": r.badge,
                "full_name": r.full_name,
                "department": r.department,
            }
            for r in rows
        ]
    }


@router.get("/{employee_id}")
def get_employee_endpoint(employee_id: int, db: Session = Depends(get_db)):
    emp = get_employee(db, employee_id)
    if emp is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado.")
    return emp
