from datetime import datetime
from pydantic import BaseModel, ConfigDict

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int
    created_at: datetime

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    pass

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    user_id: int | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


    