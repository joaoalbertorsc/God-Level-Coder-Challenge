from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List, Optional, Dict, Any
from repositories.sales_repository import SalesRepository
from models.sales import (
    SalesOverviewResponse, 
    TopProductsResponse, 
    TopProduct,
    SalesByDimensionResponse,
    SalesByDimensionItem,
    DeliveryPerformanceResponse,
    DeliveryPerformanceItem,
    TicketTrendResponse,
    TimeSeriesDataPoint,
    TicketCompositionItem,
    TicketCompositionResponse
)
from cache import get_from_cache, set_in_cache
from dateutil.relativedelta import relativedelta

class SalesService:
    def __init__(self, db: Session):
        self.sales_repository = SalesRepository(db)

    def get_sales_overview(self, start_date: date, end_date: date) -> SalesOverviewResponse:
        cache_key = f"sales_overview:{start_date}:{end_date}"
        cached_data = get_from_cache(cache_key)

        if cached_data:
            return SalesOverviewResponse(**cached_data)

        overview_data = self.sales_repository.get_sales_overview(start_date, end_date)
        response = SalesOverviewResponse(
            total_revenue=float(overview_data.get('total_revenue', 0)),
            total_sales_count=int(overview_data.get('total_sales_count', 0)),
            average_ticket_value=float(overview_data.get('average_ticket_value', 0)),
            start_date=start_date,
            end_date=end_date
        )

        set_in_cache(cache_key, response.model_dump(mode='json'))
        return response

    def get_monthly_summary(self) -> Dict[str, Any]:
        today = date.today()
        cache_key = f"monthly_summary:{today.strftime('%Y-%m-%d')}"
        cached_data = get_from_cache(cache_key)
        if cached_data:
            return cached_data

        start_of_current_month = today.replace(day=1)
        current_month_overview = self.sales_repository.get_sales_overview(start_date=start_of_current_month, end_date=today)
        current_month_revenue = current_month_overview.get('total_revenue') or 0.0

        start_of_previous_month = start_of_current_month - relativedelta(months=1)
        end_of_previous_month_same_day = min(today.replace(month=start_of_previous_month.month, year=start_of_previous_month.year), start_of_previous_month + relativedelta(months=1) - timedelta(days=1))
        
        previous_month_overview_same_day = self.sales_repository.get_sales_overview(start_date=start_of_previous_month, end_date=end_of_previous_month_same_day)
        previous_month_revenue_same_day = previous_month_overview_same_day.get('total_revenue') or 0.0

        total_revenue_last_3_full_months = 0.0
        for i in range(1, 4):
            month_end = start_of_current_month - relativedelta(months=i, days=1)
            month_start = month_end.replace(day=1)
            
            monthly_overview = self.sales_repository.get_sales_overview(start_date=month_start, end_date=month_end)
            total_revenue_last_3_full_months += monthly_overview.get('total_revenue') or 0.0
        
        last_3_months_avg_revenue = (total_revenue_last_3_full_months / 3) if total_revenue_last_3_full_months > 0 else 0.0

        response = {
            "current_month_revenue": current_month_revenue,
            "previous_month_revenue_same_day": previous_month_revenue_same_day,
            "last_3_months_avg_revenue": last_3_months_avg_revenue,
        }

        set_in_cache(cache_key, response)
        return response

    def get_top_products(
        self, 
        start_date: date, 
        end_date: date, 
        limit: int, 
        channel_id: Optional[int] = None, 
        store_id: Optional[int] = None,
        day_of_week: Optional[int] = None,
        start_hour: Optional[int] = None,
        end_hour: Optional[int] = None
    ) -> TopProductsResponse:
        cache_key = f"top_products:{start_date}:{end_date}:{limit}:{channel_id}:{store_id}:{day_of_week}:{start_hour}:{end_hour}"
        cached_data = get_from_cache(cache_key)

        if cached_data:
            return TopProductsResponse(**cached_data)

        top_products_data = self.sales_repository.get_top_products(
            start_date=start_date, 
            end_date=end_date, 
            limit=limit, 
            channel_id=channel_id, 
            store_id=store_id,
            day_of_week=day_of_week,
            start_hour=start_hour,
            end_hour=end_hour
        )

        top_products = [TopProduct(**product_data) for product_data in top_products_data]
        response = TopProductsResponse(
            start_date=start_date,
            end_date=end_date,
            top_products=top_products
        )

        set_in_cache(cache_key, response.model_dump(mode='json'))
        return response

    def get_sales_breakdown(self, start_date: date, end_date: date, dimension: str) -> SalesByDimensionResponse:
        cache_key = f"sales_breakdown:{start_date}:{end_date}:{dimension}"
        cached_data = get_from_cache(cache_key)

        if cached_data:
            return SalesByDimensionResponse(**cached_data)

        breakdown_data = self.sales_repository.get_sales_breakdown_by_dimension(
            start_date=start_date, 
            end_date=end_date, 
            dimension=dimension
        )

        breakdown_items = [SalesByDimensionItem(**item) for item in breakdown_data]
        response = SalesByDimensionResponse(
            start_date=start_date,
            end_date=end_date,
            dimension=dimension,
            breakdown=breakdown_items
        )

        set_in_cache(cache_key, response.model_dump(mode='json'))
        return response

    def get_delivery_performance(self, start_date: date, end_date: date, dimension: str, day_of_week: Optional[int] = None, start_hour: Optional[int] = None, end_hour: Optional[int] = None) -> DeliveryPerformanceResponse:
        cache_key = f"delivery_performance:{start_date}:{end_date}:{dimension}:{day_of_week}:{start_hour}:{end_hour}"
        cached_data = get_from_cache(cache_key)

        if cached_data:
            return DeliveryPerformanceResponse(**cached_data)

        performance_data = self.sales_repository.get_delivery_performance_by_dimension(
            start_date=start_date, 
            end_date=end_date, 
            dimension=dimension,
            day_of_week=day_of_week,
            start_hour=start_hour,
            end_hour=end_hour
        )

        performance_items = [DeliveryPerformanceItem(**item) for item in performance_data]
        response = DeliveryPerformanceResponse(
            start_date=start_date,
            end_date=end_date,
            dimension=dimension,
            performance_breakdown=performance_items
        )

        set_in_cache(cache_key, response.model_dump(mode='json'))
        return response

    def get_ticket_trend(self, start_date: date, end_date: date) -> TicketTrendResponse:
        cache_key = f"ticket_trend:{start_date}:{end_date}"
        cached_data = get_from_cache(cache_key)

        if cached_data:
            return TicketTrendResponse(**cached_data)

        trend_data = self.sales_repository.get_ticket_trend(start_date, end_date)
        
        response = TicketTrendResponse(
            start_date=start_date,
            end_date=end_date,
            trend=[TimeSeriesDataPoint(**point) for point in trend_data]
        )

        set_in_cache(cache_key, response.model_dump(mode='json'))
        return response

    def get_ticket_composition(self, start_date: date, end_date: date) -> TicketCompositionResponse:
        cache_key = f"ticket_composition:{start_date}:{end_date}"
        cached_data = get_from_cache(cache_key)

        if cached_data:
            return TicketCompositionResponse(**cached_data)

        composition_data = self.sales_repository.get_sales_composition_by_category(start_date, end_date)
        
        composition_items = [TicketCompositionItem(**item) for item in composition_data]
        response = TicketCompositionResponse(
            start_date=start_date,
            end_date=end_date,
            composition=composition_items
        )

        set_in_cache(cache_key, response.model_dump(mode='json'))
        return response
