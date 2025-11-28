from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LogBase(BaseModel):
    habit_id : int
    notes : Optional[str] = None

class LogCreate(LogBase):
    pass

class LogInDB(LogBase):
    id : int
    completed_at : datetime


class LogResponse(LogInDB):
    pass 