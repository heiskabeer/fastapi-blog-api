from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime
    user_type_id: Literal[1,2]


class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    user_type_id: Literal[1,2]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    user_type_id: int | None = None

