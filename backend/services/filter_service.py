from sqlalchemy.orm import Session
from repositories.filter_repository import FilterRepository
from models.filters import FilterOptionsResponse, Channel, Store

class FilterService:
    def __init__(self, db: Session):
        self.filter_repository = FilterRepository(db)

    def get_filter_options(self) -> FilterOptionsResponse:
        channels_data = self.filter_repository.get_all_channels()
        stores_data = self.filter_repository.get_all_stores()

        channels = [Channel(**ch) for ch in channels_data]
        stores = [Store(**st) for st in stores_data]

        return FilterOptionsResponse(channels=channels, stores=stores)
