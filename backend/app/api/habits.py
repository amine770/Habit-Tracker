from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.habit import HabitResponse, HabitCreate, HabitUpdate
from app.schemas.user import UserInDBBase
from app.services.habit_service import HabitServices
from app.models.habit import Habit
from app.core.security import get_current_user
from app.db.session import get_db
from typing import List

router = APIRouter(tags=["Habits"], prefix="/habit")

@router.post("", response_model=HabitResponse)
def create_habit(habit : HabitCreate, user : UserInDBBase = Depends(get_current_user), db : Session = Depends(get_db)):
    return HabitServices.create_habit(db, user.id, habit)

@router.get("", response_model=List[HabitResponse])
def get_user_habits(
    limit: int = 1,
    is_active: bool | None = None,
    user: UserInDBBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return HabitServices.get_user_habits(db, user.id, is_active, limit)


@router.get("/{id}", response_model=HabitResponse)
def get_habit_by_id(id: int, user: UserInDBBase = Depends(get_current_user), db: Session = Depends(get_db)):
    return HabitServices.get_habit_by_id(db, user.id, id)

@router.put("/{id}", response_model=HabitResponse)
def update_habit(id: int, data: HabitUpdate, user: UserInDBBase = Depends(get_current_user), db: Session = Depends(get_db)):
    return HabitServices.update_habit(db, user.id, id, data)

@router.delete("/{id}")
def delete_habit(id: int, user: UserInDBBase = Depends(get_current_user), db: Session = Depends(get_db)):
    HabitServices.delete_habit(db, user.id, id)
    return {"message": "habit deleted successfully"}