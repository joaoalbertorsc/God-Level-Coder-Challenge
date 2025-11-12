from sqlalchemy.orm import Session
from sqlalchemy import text

class GoalRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_average_ticket_goal(self) -> float:
        query = text("SELECT goal_value FROM goals WHERE goal_name = 'average_ticket_goal'")
        result = self.db.execute(query).scalar()
        return result if result is not None else 0.0

    def set_average_ticket_goal(self, goal_value: float):
        query = text("UPDATE goals SET goal_value = :goal_value WHERE goal_name = 'average_ticket_goal'")
        self.db.execute(query, {"goal_value": goal_value, "goal_name": "average_ticket_goal"})
        self.db.commit()
