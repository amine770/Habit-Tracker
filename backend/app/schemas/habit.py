from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HabitBase(BaseModel):
    name : str
    description : Optional[str] = None
    frequency : str = "daily"
    color : str = "blue"
    icon : Optional[str] = None
    is_active : bool = True

class HabitCreate(HabitBase):
    pass


class HabitUpdate(HabitBase):
    name : Optional[str] = None
    description : Optional[str] = None
    frequency : Optional[str] = None
    color : Optional[str] = None
    icon : Optional[str] = None
    is_active : Optional[bool] = None


class HabitInDB(HabitBase):
    id : int
    user_id : int
    created_at : datetime
    updated_at : datetime

    class Config:
        from_attributes = True

class HabitResponse(HabitInDB):
    pass