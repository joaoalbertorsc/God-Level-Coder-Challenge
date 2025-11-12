from sqlalchemy.orm import Session
from sqlalchemy import text

class HealthRepository:
    def __init__(self, db: Session):
        self.db = db

    def check_db_connection(self) -> bool:
        try:
            self.db.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
