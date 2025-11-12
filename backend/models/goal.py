from pydantic import BaseModel
from typing import Optional

class AverageTicketGoal(BaseModel):
    id: Optional[int] = None
    goal_value: float
