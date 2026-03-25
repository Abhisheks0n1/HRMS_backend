from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.db import Base

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    department = Column(String(50), nullable=False)


    attendances = relationship("Attendance", back_populates="employee", cascade="all, delete")