from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitUpdate



class HabitServices:
    @staticmethod
    def create_habit(db: Session, user_id: int, data: HabitCreate) -> Habit:
        if db.query(Habit).filter(Habit.user_id == user_id, Habit.name == data.name).first():
            raise HTTPException(status_code=400, detail="Habit name already exists for this user")
        habit = Habit(**data.dict(), user_id=user_id)
        db.add(habit)
        db.commit()
        db.refresh(habit)
        return habit

    @staticmethod
    def get_user_habits(db: Session, user_id: int, is_active: bool | None = None, limit: int | None = None) -> list[Habit]:
        q = db.query(Habit).filter(Habit.user_id == user_id)
        if is_active is not None:
            q = q.filter(Habit.is_active == is_active)
        q = q.order_by(Habit.created_at.desc())
        if limit:
            q = q.limit(limit)
        return q.all()

    @staticmethod
    def get_habit_by_id(db: Session, user_id: int, habit_id: int) -> Habit | None:
        return db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user_id).first()

    @staticmethod
    def update_habit(db: Session, user_id: int, habit_id: int, data: HabitUpdate) -> Habit:
        habit = HabitServices.get_habit_by_id(db, user_id, habit_id)
        if not habit:
            raise HTTPException(status_code=404, detail="Habit not found")
        for key, value in data.dict(exclude_unset=True).items():
            setattr(habit, key, value)
        db.commit()
        db.refresh(habit)
        return habit

    @staticmethod
    def delete_habit(db: Session, user_id: int, habit_id: int) -> None:
        habit = HabitServices.get_habit_by_id(db, user_id, habit_id)
        if not habit:
            raise HTTPException(status_code=404, detail="Habit not found")
        db.delete(habit)
        db.commit()


