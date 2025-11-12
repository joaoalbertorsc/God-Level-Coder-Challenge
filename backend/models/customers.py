from pydantic import BaseModel
from datetime import date
from typing import List

class ChurnRiskCustomer(BaseModel):
    customer_id: int
    customer_name: str
    total_purchases: int
    last_purchase_date: date

class CustomerChurnRiskResponse(BaseModel):
    min_purchases: int
    inactive_days: int
    churn_risk_customers: List[ChurnRiskCustomer]
