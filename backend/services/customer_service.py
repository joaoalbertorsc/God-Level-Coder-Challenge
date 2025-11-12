from sqlalchemy.orm import Session
from repositories.customer_repository import CustomerRepository
from models.customers import CustomerChurnRiskResponse, ChurnRiskCustomer
from cache import get_from_cache, set_in_cache

class CustomerService:
    def __init__(self, db: Session):
        self.customer_repository = CustomerRepository(db)

    def get_churn_risk_customers(self, min_purchases: int, inactive_days: int) -> CustomerChurnRiskResponse:
        cache_key = f"churn_risk:{min_purchases}:{inactive_days}"
        cached_data = get_from_cache(cache_key)

        if cached_data:
            return CustomerChurnRiskResponse(**cached_data)

        churn_risk_data = self.customer_repository.get_churn_risk_customers(
            min_purchases=min_purchases, 
            inactive_days=inactive_days
        )

        churn_risk_customers = [ChurnRiskCustomer(**customer) for customer in churn_risk_data]
        response = CustomerChurnRiskResponse(
            min_purchases=min_purchases,
            inactive_days=inactive_days,
            churn_risk_customers=churn_risk_customers
        )

        set_in_cache(cache_key, response.model_dump(mode='json'))
        return response
