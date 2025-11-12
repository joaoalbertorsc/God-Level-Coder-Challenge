from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.health_service import HealthService
from models.common import HealthCheckResponse

router = APIRouter()

@router.get("/", response_model=dict)
async def read_root():
    return {"message": "Welcome to the God Level Analytics API!"}

@router.get("/health", response_model=HealthCheckResponse)
async def health_check(db: Session = Depends(get_db)):
    health_service = HealthService(db)
    status = health_service.get_health_status()
    if status.database == "disconnected":
        raise HTTPException(status_code=500, detail="Database connection failed")
    return status
