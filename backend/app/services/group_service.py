from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.schemas.group import GroupCreate, GroupUpdate, HabitSummary
from app.models.group import Group
from app.models.habit_log import HabitLog
from app.models.habit import Habit
from datetime import datetime, date, timedelta

class GroupServices:
    @staticmethod
    def create_group(db: Session, current_user_id: int, data: GroupCreate):
        group = Group(**data.dict(), user_id = current_user_id)
        db.add(group)
        db.commit()
        db.refresh(group)
        return group
    
    @staticmethod
    def update_group(db: Session, current_user_id:int, group_id: int, data: GroupUpdate):
        group = db.query(Group).filter(Group.id == group_id, Group.user_id == current_user_id).first()
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="group not found")
        
        for field, value in data.dict(exclude_unset=True).items():
            setattr(group, field, value)
        db.commit()
        db.refresh(group)
        return group
    
    @staticmethod
    def delete_group(db: Session, group_id: int, current_user_id: int):
        group = db.query(Group).filter(Group.id == group_id, Group.user_id == current_user_id).first()
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="group not found")
        db.delete(group)
        db.commit()
        return {"message" : "group deleted successfully"}
    
    def get_group_detail(self, db: Session, group_id: int, current_user_id: int):
        group = db.query(Group).filter(Group.id == group_id, Group.user_id == current_user_id).first()
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="group not found")
        
        habits_summary = []
        for habit in group.habits:
            streak = self.compute_streak(db, habit)
            rate = self.completion_rate(db, habit)
            habit = HabitSummary(
                id = habit.id, 
                name = habit.name,
                frequency= habit.frequency, 
                streak = streak,
                completion_rate = rate,
            )
            habits_summary.append(habit)

            return{
                "id": group.id,
                "name": group.name,
                "description": group.description,
                "habits": habits_summary,
                "total_habits": len(habits_summary)
            }

    @staticmethod    
    def compute_streak(db: Session, habit: Habit):
        logs = db.query(HabitLog).filter(HabitLog.habit_id == habit.id).order_by(HabitLog.completed_at.desc()).all()
        
        streak = 0
        cur_day = date.today()
        for log in logs:
            if log.completed_at.date() == cur_day:
                counter += 1
                cur_day = cur_day.replace(day=cur_day.day -1 )
            else:
                break
        return streak
    
    @staticmethod
    def completion_rate(db: Session, habit: Habit):
        thirty_days_ago = datetime.now() - timedelta(days=30)
        num_logs = db.query(HabitLog).filter(HabitLog.habit_id == habit.id, func.date(HabitLog.completed_at) >= thirty_days_ago).count()

        return (num_logs * 30)/100
    
group_service = GroupServices()

    
