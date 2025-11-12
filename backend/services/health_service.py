from sqlalchemy.orm import Session
from repositories.health_repository import HealthRepository
from models.common import HealthCheckResponse

class HealthService:
    def __init__(self, db: Session):
        self.health_repository = HealthRepository(db)

    def get_health_status(self) -> HealthCheckResponse:
        is_db_connected = self.health_repository.check_db_connection()
        db_status = "connected" if is_db_connected else "disconnected"
        return HealthCheckResponse(status="ok", database=db_status)
