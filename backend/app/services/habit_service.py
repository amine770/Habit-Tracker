from sqlalchemy.orm import Session
from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitUpdate, HabitInDB



class HabitServices:
    @staticmethod
    def create_habit(db : Session, user_id : int, data : HabitCreate):
        habit = Habit(**data.dict(), user_id = user_id)
        db.add(habit)
        db.commit()
        db.refresh()
        return habit
    
    @staticmethod
    def get_user_habits(db : Session, user_id : int):
        return db.query(Habit).filter(Habit.user_id == user_id).all()
    
    @staticmethod
    def get_habit_by_id(db : Session, id : int):
        return db.query(Habit).filter(Habit.id == id).first()
    
    @staticmethod
    def update_habit(db : Session, id : int, data : HabitUpdate, habit : HabitInDB):
        for key, valu in data.dict(exclude_unset=True).items():
            setattr(habit, key, valu)

        db.commit()
        db.refresh(habit)
        return habit
    
    @staticmethod
    def delete_habit(db : Session, habit : HabitInDB):
        db.delete(habit)
        db.commit()


