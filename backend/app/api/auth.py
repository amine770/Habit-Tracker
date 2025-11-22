from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.token import Token
from app.schemas.user import UserResponse, UserCreate
from app.db.session import get_db
from app.models.user import User 
from app.core.security  import verify_password, create_token, get_hash_password


router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username ).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    elif not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    access_token = create_token(data = {"user_id" :user.id})
    return {"access_token" : access_token, "token_type" : "Bearer"}

@router.post("/register",  response_model=UserResponse)
def register(user : UserCreate, db : Session = Depends(get_db)):
    user.hashed_password = get_hash_password(user.hashed_password)
    
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    