from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date, timedelta
from typing import List, Optional

class SalesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_sales_overview(self, start_date: date, end_date: date) -> dict:
        query = text("""
            SELECT
                COALESCE(SUM(s.total_amount), 0) as total_revenue,
                COALESCE(COUNT(s.id), 0) as total_sales_count,
                COALESCE(AVG(s.total_amount), 0) as average_ticket_value
            FROM sales s
            WHERE s.sale_status_desc = 'COMPLETED'
              AND s.created_at >= :start_date
              AND s.created_at < :end_date_plus_one
        """)
        result = self.db.execute(query, {
            "start_date": start_date,
            "end_date_plus_one": end_date + timedelta(days=1)
        }).fetchone()
        return result._asdict() if result else {
            "total_revenue": 0,
            "total_sales_count": 0,
            "average_ticket_value": 0
        }

    def get_top_products(self, start_date: date, end_date: date, limit: int, channel_id: Optional[int] = None, store_id: Optional[int] = None, day_of_week: Optional[int] = None, start_hour: Optional[int] = None, end_hour: Optional[int] = None) -> List[dict]:
        params = {
            "start_date": start_date,
            "end_date_plus_one": end_date + timedelta(days=1),
            "limit": limit
        }
        query_str = """
            SELECT
                p.id as product_id,
                p.name as product_name,
                SUM(ps.total_price) as total_revenue,
                SUM(ps.quantity) as total_sales_count
            FROM product_sales ps
            JOIN products p ON ps.product_id = p.id
            JOIN sales s ON ps.sale_id = s.id
            WHERE s.sale_status_desc = 'COMPLETED'
              AND s.created_at >= :start_date
              AND s.created_at < :end_date_plus_one
        """
        if channel_id:
            query_str += " AND s.channel_id = :channel_id"
            params["channel_id"] = channel_id
        if store_id:
            query_str += " AND s.store_id = :store_id"
            params["store_id"] = store_id
        if day_of_week is not None:
            query_str += " AND EXTRACT(ISODOW FROM s.created_at) = :day_of_week"
            params["day_of_week"] = day_of_week
        if start_hour is not None and end_hour is not None:
            query_str += " AND EXTRACT(HOUR FROM s.created_at) BETWEEN :start_hour AND :end_hour"
            params["start_hour"] = start_hour
            params["end_hour"] = end_hour
        query_str += """
            GROUP BY p.id, p.name
            ORDER BY total_revenue DESC
            LIMIT :limit
        """
        query = text(query_str)
        results = self.db.execute(query, params).fetchall()
        return [result._asdict() for result in results]

    def get_sales_breakdown_by_dimension(self, start_date: date, end_date: date, dimension: str) -> List[dict]:
        if dimension not in ['channel', 'store']:
            raise ValueError("Invalid dimension specified. Must be 'channel' or 'store'.")
        dimension_table = "channels" if dimension == 'channel' else "stores"
        dimension_fk = f"{dimension}_id"
        query = text(f"""
            SELECT
                d.id as dimension_id,
                d.name as dimension_name,
                COALESCE(SUM(s.total_amount), 0) as total_revenue,
                COALESCE(COUNT(s.id), 0) as total_sales_count,
                COALESCE(AVG(s.total_amount), 0) as average_ticket_value
            FROM sales s
            JOIN {dimension_table} d ON s.{dimension_fk} = d.id
            WHERE s.sale_status_desc = 'COMPLETED'
              AND s.created_at >= :start_date
              AND s.created_at < :end_date_plus_one
            GROUP BY d.id, d.name
            ORDER BY total_revenue DESC
        """)
        params = {
            "start_date": start_date,
            "end_date_plus_one": end_date + timedelta(days=1)
        }
        results = self.db.execute(query, params).fetchall()
        return [result._asdict() for result in results]

    def get_delivery_performance_by_dimension(self, start_date: date, end_date: date, dimension: str, day_of_week: Optional[int] = None, start_hour: Optional[int] = None, end_hour: Optional[int] = None) -> List[dict]:
        if dimension not in ['store', 'neighborhood', 'city']:
            raise ValueError("Invalid dimension for delivery performance.")

        params = {
            "start_date": start_date,
            "end_date_plus_one": end_date + timedelta(days=1)
        }

        group_by_clause = ""
        if dimension == 'store':
            group_by_clause = "st.name"
        elif dimension == 'neighborhood':
            group_by_clause = "da.neighborhood"
        elif dimension == 'city':
            group_by_clause = "da.city"

        where_clauses = [
            "s.sale_status_desc = 'COMPLETED'",
            "s.delivery_seconds IS NOT NULL",
            "s.created_at >= :start_date",
            "s.created_at < :end_date_plus_one"
        ]

        if day_of_week is not None:
            where_clauses.append("EXTRACT(ISODOW FROM s.created_at) = :day_of_week")
            params["day_of_week"] = day_of_week
        if start_hour is not None and end_hour is not None:
            where_clauses.append("EXTRACT(HOUR FROM s.created_at) BETWEEN :start_hour AND :end_hour")
            params["start_hour"] = start_hour
            params["end_hour"] = end_hour

        where_sql = " AND ".join(where_clauses)

        query = text(f"""
            SELECT
                {group_by_clause} as dimension_name,
                COALESCE(AVG(s.delivery_seconds), 0) as average_delivery_seconds,
                COALESCE(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY s.delivery_seconds), 0) as p90_delivery_seconds,
                COUNT(s.id) as total_deliveries
            FROM sales s
            JOIN delivery_addresses da ON s.id = da.sale_id
            LEFT JOIN stores st ON s.store_id = st.id
            WHERE {where_sql}
            GROUP BY {group_by_clause}
            HAVING COUNT(s.id) >= 10
            ORDER BY average_delivery_seconds DESC;
        """)
        
        results = self.db.execute(query, params).fetchall()
        return [result._asdict() for result in results]

    def get_ticket_trend(self, start_date: date, end_date: date) -> List[dict]:
        query = text("""
            SELECT
                DATE(s.created_at) as date,
                COALESCE(AVG(s.total_amount), 0) as value
            FROM sales s
            WHERE s.sale_status_desc = 'COMPLETED'
              AND s.created_at >= :start_date
              AND s.created_at < :end_date_plus_one
            GROUP BY DATE(s.created_at)
            ORDER BY date ASC
        """)
        params = {
            "start_date": start_date,
            "end_date_plus_one": end_date + timedelta(days=1)
        }
        results = self.db.execute(query, params).fetchall()
        return [result._asdict() for result in results]

    def get_sales_composition_by_category(self, start_date: date, end_date: date) -> List[dict]:
        query = text("""
            SELECT
                c.name as category_name,
                COALESCE(SUM(ps.total_price), 0) as total_revenue
            FROM sales s
            JOIN product_sales ps ON s.id = ps.sale_id
            JOIN products p ON ps.product_id = p.id
            JOIN categories c ON p.category_id = c.id
            WHERE s.sale_status_desc = 'COMPLETED'
              AND s.created_at >= :start_date
              AND s.created_at < :end_date_plus_one
            GROUP BY c.name
            ORDER BY total_revenue DESC
        """)
        params = {
            "start_date": start_date,
            "end_date_plus_one": end_date + timedelta(days=1)
        }
        results = self.db.execute(query, params).fetchall()
        return [result._asdict() for result in results]
