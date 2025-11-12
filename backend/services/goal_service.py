from sqlalchemy.orm import Session
from repositories.goal_repository import GoalRepository

class GoalService:
    def __init__(self, db: Session):
        self.goal_repository = GoalRepository(db)

    def get_goal(self) -> float:
        return self.goal_repository.get_average_ticket_goal()

    def update_goal(self, goal_value: float):
        self.goal_repository.set_average_ticket_goal(goal_value)
