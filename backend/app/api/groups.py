from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.group import GroupResponse, GroupCreate, GroupUpdate
from app.schemas.user import UserInDBBase
from app.services.group_service import group_service
from app.db.session import get_db
from app.core.security import get_current_user

router = APIRouter(tags=["Groups"], prefix="/group")

@router.post("", response_model=GroupResponse)
def create_group(data: GroupCreate, user: UserInDBBase = Depends(get_current_user)  ,db: Session = Depends(get_db)):
    return group_service.create_group(db, user.id, data)

@router.put("/{id}", response_model=GroupResponse)
def update_group(id: int, data: GroupUpdate, current_user: UserInDBBase = Depends(get_current_user) ,db: Session = Depends(get_db)):
    return group_service.update_group(db, current_user.id, id, data)

@router.get("/{id}", response_model=GroupResponse)
def get_group(id: int, current_user: UserInDBBase = Depends(get_current_user)  ,db: Session = Depends(get_db)):
    return group_service.get_group_detail(db, id, current_user.id)

@router.delete("/{id}")
def delete_group(id: int, current_user: UserInDBBase = Depends(get_current_user) ,db: Session = Depends(get_db)):
    return group_service.delete_group(db, id, current_user.id)