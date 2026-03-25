from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.models.employee import Employee
from app.models.attendance import Attendance
from app.schemas.employee import EmployeeCreate, EmployeeRead
from app.controllers.employee import (
    get_employees, create_employee, delete_employee,
    get_employee_by_id, update_employee
)

from app.config.db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_new_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    if get_employee_by_id(db, employee.employee_id):
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    return create_employee(db, employee)


@router.get("/", response_model=List[EmployeeRead])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_employees(db, skip, limit)


@router.put("/{employee_id}", response_model=EmployeeRead)
def update_employee_route(employee_id: str, employee_update: EmployeeCreate, db: Session = Depends(get_db)):
    existing = get_employee_by_id(db, employee_update.employee_id)
    if existing and existing.employee_id != employee_id:
        raise HTTPException(status_code=400, detail="Employee ID already taken by another employee")
    
    return update_employee(db, employee_id, employee_update.model_dump())


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee_route(employee_id: str, db: Session = Depends(get_db)):
    if not delete_employee(db, employee_id):
        raise HTTPException(status_code=404, detail="Employee not found")
    return None


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_employees = db.query(Employee).count()
    today = date.today()
    present_today = db.query(Attendance).filter(
        Attendance.date == today, 
        Attendance.status == "Present"
    ).count()

    return {
        "total_employees": total_employees,
        "present_today": present_today
    }