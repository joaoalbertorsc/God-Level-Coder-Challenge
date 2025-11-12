from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.filter_service import FilterService
from models.filters import FilterOptionsResponse

router = APIRouter(
    prefix="/filters",
    tags=["Filters"]
)

@router.get("/options", response_model=FilterOptionsResponse)
async def get_filter_options(db: Session = Depends(get_db)):
    filter_service = FilterService(db)
    return filter_service.get_filter_options()
