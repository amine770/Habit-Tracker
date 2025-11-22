from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None


class UserInDBBase(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserResponse(UserInDBBase):
    username: str
    email: str


class UserInDB(UserInDBBase):
    hashed_password: str