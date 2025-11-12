from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from services.customer_service import CustomerService
from models.customers import CustomerChurnRiskResponse

router = APIRouter(
    prefix="/analytics",
    tags=["Customer Analytics"]
)

@router.get("/customer-churn-risk", response_model=CustomerChurnRiskResponse)
async def get_customer_churn_risk(
    db: Session = Depends(get_db),
    min_purchases: int = Query(default=3, ge=1, description="Minimum number of total purchases a customer must have to be considered."),
    inactive_days: int = Query(default=30, ge=1, description="Number of days since the last purchase to consider a customer inactive.")
):
    customer_service = CustomerService(db)
    churn_risk_customers = customer_service.get_churn_risk_customers(
        min_purchases=min_purchases, 
        inactive_days=inactive_days
    )
    return churn_risk_customers
