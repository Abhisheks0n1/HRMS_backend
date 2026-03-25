from pydantic import BaseModel
from datetime import date
from typing import Literal

class AttendanceCreate(BaseModel):
    employee_id: str
    date: date
    status: Literal["Present", "Absent"]

class AttendanceRead(BaseModel):
    id: int
    employee_id: str
    date: date
    status: Literal["Present", "Absent"]

    class Config:
        orm_mode = True
