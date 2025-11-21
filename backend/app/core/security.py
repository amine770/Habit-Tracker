from pwdlib import PasswordHash
from app.schemas.token import TokenData
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import Settings
from app.db.session import get_db
from fastapi.security import OAuth2PasswordBearer
from app.models import user as User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

settings = Settings()

password_hashed = PasswordHash.recommended()

def get_hash_password(password):
    return password_hashed.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hashed.verify(plain_password, hashed_password)

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes= settings.access_token_expire_minutes)
    to_encode.update({"expire" : expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not valid credentials", 
                                          headers={"WWW-Authenticate" : "Bearer"})

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        id = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = TokenData(id = id)
    except JWTError:
        raise credentials_exception 
    
    user = db.query(User).filter(User.id == token_data.id).first()
    if not user:
        
        raise credentials_exception
    return user


    

