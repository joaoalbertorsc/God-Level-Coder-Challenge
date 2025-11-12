from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import Optional, Literal, Dict, Any
from database import get_db
from services.sales_service import SalesService
from models.sales import (
    SalesOverviewResponse, 
    TopProductsResponse, 
    SalesByDimensionResponse,
    DeliveryPerformanceResponse,
    TicketTrendResponse,
    TicketCompositionResponse
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/monthly-summary", response_model=Dict[str, Any])
async def get_monthly_summary(db: Session = Depends(get_db)):
    sales_service = SalesService(db)
    return sales_service.get_monthly_kpis()

@router.get("/sales-overview", response_model=SalesOverviewResponse)
async def get_sales_overview(
    db: Session = Depends(get_db),
    start_date: date = Query(default=date.today() - timedelta(days=30), description="Start date for the analysis period (YYYY-MM-DD)"),
    end_date: date = Query(default=date.today(), description="End date for the analysis period (YYYY-MM-DD)")
):
    sales_service = SalesService(db)
    overview = sales_service.get_sales_overview(start_date=start_date, end_date=end_date)
    return overview

@router.get("/top-products", response_model=TopProductsResponse)
async def get_top_products(
    db: Session = Depends(get_db),
    start_date: date = Query(default=date.today() - timedelta(days=30), description="Start date for the analysis period (YYYY-MM-DD)"),
    end_date: date = Query(default=date.today(), description="End date for the analysis period (YYYY-MM-DD)"),
    limit: int = Query(default=10, ge=1, le=100, description="The number of top products to return"),
    channel_id: Optional[int] = Query(default=None, description="Filter by a specific sales channel ID"),
    store_id: Optional[int] = Query(default=None, description="Filter by a specific store ID"),
    day_of_week: Optional[int] = Query(default=None, ge=1, le=7, description="Filter by day of the week (1=Monday, 7=Sunday)"),
    start_hour: Optional[int] = Query(default=None, ge=0, le=23, description="Start of the hour range (0-23)"),
    end_hour: Optional[int] = Query(default=None, ge=0, le=23, description="End of the hour range (0-23)")
):
    if (start_hour is not None and end_hour is None) or (start_hour is None and end_hour is not None):
        raise HTTPException(status_code=400, detail="Both start_hour and end_hour must be provided for time-based filtering.")

    sales_service = SalesService(db)
    top_products = sales_service.get_top_products(
        start_date=start_date, 
        end_date=end_date, 
        limit=limit, 
        channel_id=channel_id, 
        store_id=store_id,
        day_of_week=day_of_week,
        start_hour=start_hour,
        end_hour=end_hour
    )
    return top_products

@router.get("/sales-breakdown", response_model=SalesByDimensionResponse)
async def get_sales_breakdown(
    db: Session = Depends(get_db),
    dimension: Literal['channel', 'store'] = Query(description="The dimension to break down sales by ('channel' or 'store')"),
    start_date: date = Query(default=date.today() - timedelta(days=30), description="Start date for the analysis period (YYYY-MM-DD)"),
    end_date: date = Query(default=date.today(), description="End date for the analysis period (YYYY-MM-DD)")
):
    try:
        sales_service = SalesService(db)
        breakdown = sales_service.get_sales_breakdown(
            start_date=start_date, 
            end_date=end_date, 
            dimension=dimension
        )
        return breakdown
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/delivery-performance", response_model=DeliveryPerformanceResponse)
async def get_delivery_performance(
    db: Session = Depends(get_db),
    dimension: Literal['store', 'neighborhood', 'city'] = Query(description="The dimension to analyze delivery performance by ('store' or 'neighborhood')"),
    start_date: date = Query(default=date.today() - timedelta(days=30), description="Start date for the analysis period (YYYY-MM-DD)"),
    end_date: date = Query(default=date.today(), description="End date for the analysis period (YYYY-MM-DD)"),
    day_of_week: Optional[int] = Query(default=None, ge=1, le=7, description="Filter by day of the week (1=Monday, 7=Sunday)"),
    start_hour: Optional[int] = Query(default=None, ge=0, le=23, description="Start of the hour range (0-23)"),
    end_hour: Optional[int] = Query(default=None, ge=0, le=23, description="End of the hour range (0-23)")
):
    if (start_hour is not None and end_hour is None) or (start_hour is None and end_hour is not None):
        raise HTTPException(status_code=400, detail="Both start_hour and end_hour must be provided for time-based filtering.")

    try:
        sales_service = SalesService(db)
        performance = sales_service.get_delivery_performance(
            start_date=start_date, 
            end_date=end_date, 
            dimension=dimension,
            day_of_week=day_of_week,
            start_hour=start_hour,
            end_hour=end_hour
        )
        return performance
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/ticket-trend", response_model=TicketTrendResponse)
async def get_ticket_trend(
    db: Session = Depends(get_db),
    start_date: date = Query(default=date.today() - timedelta(days=30), description="Start date for the analysis period (YYYY-MM-DD)"),
    end_date: date = Query(default=date.today(), description="End date for the analysis period (YYYY-MM-DD)")
):
    sales_service = SalesService(db)
    return sales_service.get_ticket_trend(start_date=start_date, end_date=end_date)

@router.get("/ticket-composition", response_model=TicketCompositionResponse)
async def get_ticket_composition(
    db: Session = Depends(get_db),
    start_date: date = Query(default=date.today() - timedelta(days=30), description="Start date for the analysis period (YYYY-MM-DD)"),
    end_date: date = Query(default=date.today(), description="End date for the analysis period (YYYY-MM-DD)")
):
    sales_service = SalesService(db)
    return sales_service.get_ticket_composition(start_date=start_date, end_date=end_date)
