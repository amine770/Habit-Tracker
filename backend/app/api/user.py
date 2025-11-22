from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.schemas.user import UserInDB

router = APIRouter(tags=["Users"], prefix="/user")

@router.get("/me")
def me(user : UserInDB = Depends(get_current_user)):
    return {"message" : "test done well"}