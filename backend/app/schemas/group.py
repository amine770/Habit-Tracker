from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class HabitSummary(BaseModel):
    id : int
    name : str
    frequency : str
    streak : int
    completion_rate : float

class GroupBase(BaseModel):
    name : str
    description : Optional[str] = None

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None

class GroupResponse(GroupBase):
    id : int
    name : str
    description : Optional[str] = None
    habits : List[HabitSummary]
    
    class Config:
        orm_mode = True
