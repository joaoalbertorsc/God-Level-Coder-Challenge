from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from database import get_db
from services.goal_service import GoalService
from models.goal import AverageTicketGoal

router = APIRouter(
    prefix="/goal",
    tags=["Goal"]
)

@router.get("/average-ticket-goal", response_model=AverageTicketGoal)
async def get_average_ticket_goal(db: Session = Depends(get_db)):
    goal_service = GoalService(db)
    goal_value = goal_service.get_goal()
    return AverageTicketGoal(goal_value=goal_value)

@router.put("/average-ticket-goal")
async def update_average_ticket_goal(goal: AverageTicketGoal, db: Session = Depends(get_db)):
    goal_service = GoalService(db)
    goal_service.update_goal(goal.goal_value)
    return {"message": "Goal updated successfully"}
