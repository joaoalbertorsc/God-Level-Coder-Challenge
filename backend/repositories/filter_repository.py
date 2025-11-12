from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

class FilterRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_channels(self) -> List[dict]:
        query = text("SELECT id, name FROM channels ORDER BY name ASC")
        results = self.db.execute(query).fetchall()
        return [result._asdict() for result in results]

    def get_all_stores(self) -> List[dict]:
        query = text("SELECT id, name FROM stores ORDER BY name ASC")
        results = self.db.execute(query).fetchall()
        return [result._asdict() for result in results]
