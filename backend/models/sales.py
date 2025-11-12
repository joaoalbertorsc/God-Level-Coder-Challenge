from pydantic import BaseModel
from datetime import date
from typing import List

class SalesOverviewResponse(BaseModel):
    total_revenue: float
    total_sales_count: int
    average_ticket_value: float
    start_date: date
    end_date: date

class TopProduct(BaseModel):
    product_id: int
    product_name: str
    total_revenue: float
    total_sales_count: int

class TopProductsResponse(BaseModel):
    start_date: date
    end_date: date
    top_products: List[TopProduct]

class SalesByDimensionItem(BaseModel):
    dimension_id: int
    dimension_name: str
    total_revenue: float
    total_sales_count: int
    average_ticket_value: float

class SalesByDimensionResponse(BaseModel):
    start_date: date
    end_date: date
    dimension: str
    breakdown: List[SalesByDimensionItem]

class DeliveryPerformanceItem(BaseModel):
    dimension_name: str
    average_delivery_seconds: float
    p90_delivery_seconds: float
    total_deliveries: int

class DeliveryPerformanceResponse(BaseModel):
    start_date: date
    end_date: date
    dimension: str
    performance_breakdown: List[DeliveryPerformanceItem]

class TimeSeriesDataPoint(BaseModel):
    date: date
    value: float

class TicketTrendResponse(BaseModel):
    start_date: date
    end_date: date
    trend: List[TimeSeriesDataPoint]

class TicketCompositionItem(BaseModel):
    category_name: str
    total_revenue: float

class TicketCompositionResponse(BaseModel):
    start_date: date
    end_date: date
    composition: List[TicketCompositionItem]
