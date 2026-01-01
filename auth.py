import uuid
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import Config
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from database import get_db_session
from sqlalchemy.orm import Session
from typing import Annotated

from models import UserModel


oauth2scheme= OAuth2PasswordBearer(tokenUrl="/users/login")

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(plain_password:str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    expire = datetime.now() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

def get_current_user(token:Annotated[str, Depends(oauth2scheme)], db:Annotated[Session, Depends(get_db_session)]):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
        
        user = db.query(UserModel).filter(UserModel.email == email).first()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def verify_admin(current_user: Annotated[UserModel, Depends(get_current_user)]):
    if not current_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user