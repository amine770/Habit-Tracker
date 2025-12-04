from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from app.services.analytics_service import AnalyticServices
from app.models.habit import Habit
from app.db.session import get_db
from app.core.security import get_current_user
from app.schemas.analytics import AnalyticsOverViewResponse, HabitStreakResponse, DailyProgressResponse
from app.schemas.user import UserInDBBase
from datetime import date, timedelta
from typing import List
from app.models.habit_log import HabitLog

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/overview", response_model=AnalyticsOverViewResponse)
def overview(days: int = Query(default=30),
             db: Session = Depends(get_db),
             cur_user: UserInDBBase = Depends(get_current_user)):
    
    end_day = date.today()
    start_day = end_day - timedelta(days=days -1 )
    
    habits = db.query(Habit).filter(Habit.user_id == cur_user.id, Habit.is_active == True).all()

    total_habits = db.query(Habit).filter(Habit.user_id == cur_user.id).count()
    active_habits = len(habits)
    total_complation = AnalyticServices.total_completions_user(db, cur_user.id)
    overall_rate = AnalyticServices.overall_complation_rate(db, cur_user.id, end_day, start_day)
    total_streaks = sum(AnalyticServices.calcul_streak(db, habit) for habit in habits)

    return AnalyticsOverViewResponse(
        total_habits= total_habits,
        total_active_habits= active_habits,
        total_complation= total_complation,
        total_complation_rate= overall_rate,
        total_current_streaks= total_streaks,
        date_range= {
        "start_day": start_day,
        "end_day": end_day
        }
    )

@router.get("/streaks", response_model=List[HabitStreakResponse])
def get_habit_streaks(db: Session = Depends(get_db), cur_user: UserInDBBase = Depends(get_current_user)):
    habits = db.query(Habit).filter(Habit.user_id == cur_user.id, Habit.is_active == True).all()

    streak_data = []

    for habit in habits:
        current_streak = AnalyticServices.calcul_streak(db, habit)
        longest_streak = AnalyticServices.longest_streak(db, habit)
        total_complation = AnalyticServices.total_completions(db, habit)
        streak_data.append(HabitStreakResponse(
            id= habit.id,
            name= habit.name,
            icon= habit.icon,
            color= habit.color,
            current_streak= current_streak,
            longest_streak= longest_streak,
            total_complation= total_complation
        ))
    
    streak_data.sort(key= lambda x: x.current_streak, reverse=True ) # x represent each item in the list
    return streak_data

@router.get("/daily", response_model=DailyProgressResponse)
def get_daily(target_day: date = Query(default=None),
              db: Session = Depends(get_db), cur_user: UserInDBBase = Depends(get_current_user)
              ):
    
    if not target_day:
        target_day = date.today()
    
    if target_day > date.today():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="We can't get Progress for future dates")
    
    progress = AnalyticServices.daily_progress(db, cur_user.id, target_day)
    return DailyProgressResponse(**progress)

@router.get("/habits/{habit_id}/status")
def get_habit_status(habit_id: int, 
                     days: int = Query(default=30),
                     db: Session = Depends(get_db),
                     cur_user: UserInDBBase = Depends(get_current_user)):
    
    end_day = date.today()
    start_day = end_day - timedelta(days=days -1)
    
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == cur_user.id).first()
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
    
    completion_rate = AnalyticServices.complation_rate_for_habit(db, habit, end_day, start_day)
    current_streak = AnalyticServices.calcul_streak(db, habit)
    longest_streak = AnalyticServices.longest_streak(db, habit)
    total_completion = AnalyticServices.total_completions(db, habit)

    last_log = db.query(HabitLog).filter(HabitLog.habit_id == habit.id).order_by(
        HabitLog.completed_at.desc()).first()
    
    last_log_date = last_log.completed_at.date() if last_log else None

    return {
        "habit_id": habit.id,
        "habit_name": habit.name,
        "habit_pireode": days,
        "completion_rate": completion_rate,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_completion": total_completion,
        "last_completed": last_log_date,
        "is_active": habit.is_active
    }

@router.get("/weekly-summary")
def get_weekly_summary(db: Session= Depends(get_db),
    cur_user: UserInDBBase= Depends(get_current_user)):

    weekly_summary= []
    today = date.today()
    for i in range(6, -1, -1):
        target_day = today - timedelta(days=i)
        progress = AnalyticServices.daily_progress(db, cur_user.id, target_day)

        weekly_summary.append(
            {
                "date": target_day,
                "day_name": target_day.strftime("%a"),
                "completed_habits": progress["completed"],
                "total_habits": progress["total_habits"],
                "precentage": progress["completion_percentage"]
            }
        )
    return {
        "week_start" : weekly_summary[0]["date"] if weekly_summary else None,
        "week_end" : weekly_summary[-1]["date"] if weekly_summary else None,
        "daily_progress" : weekly_summary
    }   


    






