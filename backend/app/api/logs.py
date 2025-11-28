from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.habit_log import LogResponse, LogCreate
from app.schemas.user import UserInDBBase
from app.core.security import get_current_user
from app.services.logs_service import LogsServices
from typing import List
from datetime import date

router = APIRouter(prefix="/logs",tags=["Logs"])

@router.post("", response_model=LogResponse)
def create_log(data: LogCreate, db: Session = Depends(get_db), current_user: UserInDBBase = Depends(get_current_user)):
    return LogsServices.create_log(db, data, current_user.id)

@router.delete("/{id}")
def delete_log(id: int, db: Session = Depends(get_db), current_user: UserInDBBase = Depends(get_current_user)):
    return LogsServices.delete_log(db, id,current_user.id)

@router.get("", response_model=List[LogResponse])
def get_logs_between_dates(start: date, end: date, db: Session = Depends(get_db), current_user: UserInDBBase = Depends(get_current_user)):
    return LogsServices.get_logs_between_dates(db,start,end,current_user.id)