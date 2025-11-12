from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date, timedelta
from typing import List

class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_churn_risk_customers(self, min_purchases: int, inactive_days: int) -> List[dict]:
        query = text("""
            WITH customer_purchase_summary AS (
                SELECT
                    c.id as customer_id,
                    c.customer_name,
                    COUNT(s.id) as total_purchases,
                    MAX(s.created_at)::date as last_purchase_date
                FROM customers c
                JOIN sales s ON c.id = s.customer_id
                WHERE s.sale_status_desc = 'COMPLETED'
                GROUP BY c.id, c.customer_name
            )
            SELECT
                customer_id,
                customer_name,
                total_purchases,
                last_purchase_date
            FROM customer_purchase_summary
            WHERE total_purchases >= :min_purchases
              AND last_purchase_date <= :inactive_since_date
            ORDER BY last_purchase_date ASC, total_purchases DESC;
        """)

        params = {
            "min_purchases": min_purchases,
            "inactive_since_date": date.today() - timedelta(days=inactive_days)
        }

        results = self.db.execute(query, params).fetchall()
        return [result._asdict() for result in results]
