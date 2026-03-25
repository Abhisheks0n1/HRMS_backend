from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.schemas.attendance import AttendanceCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import date
from typing import Optional, List

def create_attendance(db: Session, attendance: AttendanceCreate):
    employee = db.query(Employee).filter(Employee.employee_id == attendance.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db_att = Attendance(**attendance.dict())
    db.add(db_att)
    try:
        db.commit()
        db.refresh(db_att)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Attendance already marked for this date")
    return db_att

def get_attendances(db: Session, employee_id: Optional[str] = None,
                    start_date: Optional[date] = None, end_date: Optional[date] = None):
    query = db.query(Attendance)
    if employee_id:
        query = query.filter(Attendance.employee_id == employee_id)
    if start_date:
        query = query.filter(Attendance.date >= start_date)
    if end_date:
        query = query.filter(Attendance.date <= end_date)
    return query.all()

def get_employee_attendance_summary(db: Session, employee_id: str):
    total = db.query(Attendance).filter(Attendance.employee_id == employee_id).count()
    present = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.status == "Present"
    ).count()
    return {"total_days_marked": total, "present_days": present}
