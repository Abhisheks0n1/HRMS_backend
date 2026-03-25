from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.models.attendance import Attendance
from app.models.employee import Employee
from app.schemas.attendance import AttendanceCreate, AttendanceRead
from app.controllers.attendance import (
    create_attendance,
    get_attendances,
    get_employee_attendance_summary
)

from app.config.db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=AttendanceRead, status_code=201)
def mark_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    return create_attendance(db, attendance)


@router.get("/", response_model=List[AttendanceRead])
def read_attendances(
    employee_id: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    return get_attendances(db, employee_id, start_date, end_date)


@router.get("/summary/{employee_id}")
def attendance_summary(employee_id: str, db: Session = Depends(get_db)):
    return get_employee_attendance_summary(db, employee_id)