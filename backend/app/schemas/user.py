from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username : str
    email : str


class UserCreate(UserBase):
    hashed_password : str


class UserUpdate(BaseModel):
    username : Optional[str] = None
    email : Optional[str] = None
    hashed_password : Optional[str] = None

class UserInDBase(BaseModel):
    id : int
    created_at : datetime

    class Confing:
        orm_model = True # allwos returning sqlalchamey object

class UserResponse(UserInDBase):
    username : str
    email : str

class UserInDB(UserInDBase):
    hashed_password : str