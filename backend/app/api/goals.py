from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db
from app.api.risk import get_current_user
from app.models.models import User, Goal
from app.schemas.goal import GoalCreate, GoalResponse, GoalUpdate, GoalRoadmap
from app.services.events import event_producer
from app.services.financial_math import calculate_goal_roadmap

router = APIRouter()

@router.post("/", response_model=GoalResponse)
async def create_goal(
    goal_in: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = Goal(**goal_in.model_dump(), user_id=current_user.id)
    db.add(goal)
    db.commit()
    db.refresh(goal)

    event_producer.emit("goal_created", {
        "user_id": current_user.id,
        "goal_id": goal.id,
        "name": goal.name
    })

    return goal

@router.get("/", response_model=List[GoalResponse])
async def list_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Goal).filter(Goal.user_id == current_user.id).all()

@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

@router.patch("/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: int,
    goal_in: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    update_data = goal_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(goal, field, value)

    db.commit()
    db.refresh(goal)

    event_producer.emit("plan_recalculated", {
        "user_id": current_user.id,
        "goal_id": goal.id
    })

    return goal

@router.get("/{goal_id}/roadmap", response_model=GoalRoadmap)
async def get_goal_roadmap(
    goal_id: int,
    extra_savings: float = 0.0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    roadmap = calculate_goal_roadmap(
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        target_date=goal.target_date,
        extra_monthly_savings=extra_savings
    )
    return roadmap

@router.delete("/{goal_id}")
async def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal)
    db.commit()
    return {"status": "success"}
