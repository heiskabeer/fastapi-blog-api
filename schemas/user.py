from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
from typing import Annotated

class UserBase(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    pass

class UserOut(BaseModel):
    first_name: str
    last_name: str
    user_name:str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
