from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.db import engine, Base
from app.routers.employees import router as employees_router
from app.routers.attendance import router as attendance_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRMS Lite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees_router, prefix="/api/employees", tags=["employees"])
app.include_router(attendance_router, prefix="/api/attendance", tags=["attendance"])

@app.get("/")
def root():
    return {"message": "HRMS Lite API is running "}