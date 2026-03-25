from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Employee).offset(skip).limit(limit).all()

def get_employee_by_id(db: Session, employee_id: str):
    return db.query(Employee).filter(Employee.employee_id == employee_id).first()

def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    try:
        db.commit()
        db.refresh(db_employee)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Employee ID or Email already exists")
    return db_employee

def update_employee(db: Session, employee_id: str, updated_data: dict):
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    for key, value in updated_data.items():
        setattr(db_employee, key, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: str):
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
        return True
    return False