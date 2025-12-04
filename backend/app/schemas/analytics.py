from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class AnalyticsOverViewResponse(BaseModel):
    total_habits: int
    total_active_habits: int
    total_complation: int
    total_complation_rate: float
    total_current_streaks: int
    date_range: dict

class HabitStreakResponse(BaseModel):
    id: int
    name: str
    icon: Optional[str] = None
    color: str
    current_streak: int
    longest_streak: int
    total_complation: int

class HabitBase(BaseModel):
    id: int
    name: str
    icon: Optional[str] = None
    color: str


class DailyProgressResponse(BaseModel):
    date: date
    total_habits: int
    completed : int
    incompleted: int
    completion_percentage: float
    completed_habits: List[HabitBase]
    incompleted_habits: List[HabitBase]
