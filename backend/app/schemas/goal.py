from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.models import GoalType

class GoalBase(BaseModel):
    name: str
    type: GoalType
    target_amount: float
    current_amount: Optional[float] = 0.0
    target_date: datetime

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    target_date: Optional[datetime] = None

class GoalResponse(GoalBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class RoadmapStep(BaseModel):
    month: int
    target_savings: float
    projected_balance: float

class GoalRoadmap(BaseModel):
    monthly_savings_required: float
    roadmap: List[RoadmapStep]
