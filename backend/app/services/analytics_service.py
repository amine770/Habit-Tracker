from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from datetime import date, timedelta


class AnalyticServices:

    # ---- complation rate ----- 
    @staticmethod
    def complation_rate_for_habit(db: Session, habit: Habit, end_day: date, start_day: date):
        number_of_completion = db.query(HabitLog).filter(HabitLog.habit_id == habit.id, func.date(HabitLog.completed_at) >= start_day).count()

        total_days = (end_day - start_day).days + 1

        rate = (number_of_completion / total_days) * 100 
        return round(min(rate, 100.0), 1)
    
    @staticmethod
    def overall_complation_rate(db: Session, user_id: int, end_day: date, start_day: date):
        habits = db.query(Habit).filter(Habit.user_id == user_id).all()

        if not habits:
            return 0.0
        
        totale_rate = sum(AnalyticServices.complation_rate_for_habit(db, habit, end_day, start_day)
                          for habit in habits
        )
        return round((totale_rate / len(habits)), 1) 
    

    # ---- streak --- 
    @staticmethod
    def calcul_streak(db: Session, habit: Habit):
        logs = db.query(HabitLog).filter(HabitLog.habit_id == habit.id).order_by(HabitLog.completed_at.desc()).all()
        if not logs:
            return 0
        
        streak = 0
        cur_day = date.today()
        for log in logs:
            if log.completed_at.date() != cur_day:
                break
            else:
                streak += 1
                cur_day = cur_day - timedelta(days=1)

        return streak
    
    @staticmethod
    def longest_streak(db: Session, habit: Habit):
        logs = db.query(HabitLog).filter(HabitLog.habit_id == habit.id).order_by(HabitLog.completed_at).all()
        if not logs:
            return 0
        
        max_streak = 0
        cur_streak = 1
        for i in range(1, len(logs)):
            excepted_day = logs[i-1].completed_at + timedelta(days=1)
            if logs[i].completed_at.date() == excepted_day.date():
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 1
                
        return max(max_streak, cur_streak)
    
    # ---- daily progress ----
    @staticmethod
    def daily_progress(db: Session, user_id: int, target_date: date):
        habits = db.query(Habit).filter(Habit.user_id == user_id,
                                         Habit.is_active == True).all()
        completed_habit = []
        incompleted_habit = []

        for habit in habits:
            log_exists = db.query(HabitLog).filter(HabitLog.habit_id == habit.id, 
                                                   func.date(HabitLog.completed_at) == target_date).first() 
            habit_data = {
                "id" : habit.id,
                "name": habit.name,
                "icon": habit.icon,
                "color": habit.color
            }

            if log_exists:
                completed_habit.append(habit_data)
            else:
                incompleted_habit.append(habit_data)
            
        completed = len(completed_habit)
        total = len(habits)

        return {
            "date": target_date,
            "total_habits": total,
            "completed": completed,
            "incompleted": total - completed,
            "completion_percentage": round((completed / total) * 100, 1) if total > 0 else 0,
            "completed_habits": completed_habit,
            "incompleted_habits": incompleted_habit
        } 
 
    @staticmethod
    def total_completions(db: Session, habit: Habit):
        return db.query(HabitLog).filter(HabitLog.habit_id == habit.id).count()
    
    @staticmethod
    def total_completions_user(db: Session, user_id: int):
        return db.query(HabitLog).join(Habit).filter(Habit.user_id == user_id,
                                                     HabitLog.habit_id == Habit.id).count()




            


