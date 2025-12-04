from fastapi import HTTPException, status
from sqlalchemy import Date, cast, func
from sqlalchemy.orm import Session
from app.models.habit_log import HabitLog
from app.models.habit import Habit
from app.schemas.habit_log import LogCreate
from datetime import date


class LogsServices:
    @staticmethod
    def create_log(db: Session, data: LogCreate, current_user_id : int):
        habit = db.query(Habit).filter(Habit.user_id == current_user_id, Habit.id == data.habit_id).first()
        if not habit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"current user dont have a habit with id: {data.habit_id}")
        
        today = date.today()
        existing_log = db.query(HabitLog).filter(HabitLog.habit_id == data.habit_id, cast(HabitLog.completed_at, Date)==today).first()
        if existing_log:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="habit already completed today")
        
        log = HabitLog(**data.dict())
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    
    @staticmethod
    def delete_log(db: Session, log_id: int, current_user_id: int):
        log = db.query(HabitLog).filter(HabitLog.id == log_id).first()
        if not log:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"log not found")
        
        habit = db.query(Habit).filter(Habit.id == log.habit_id).first()
        if not habit or habit.user_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You don't have permission to delete this log")

        db.delete(log)
        db.commit()
        return {"habit deleted succesfully"}

    @staticmethod
    def get_logs_between_dates(db: Session, start: date, end: date, current_user_id: int):
        return( db.query(HabitLog)
               .join(Habit)
               .filter(Habit.user_id == current_user_id)
               .filter(func.date(HabitLog.completed_at)>=start, func.date(HabitLog.completed_at)<=end).all()
               )