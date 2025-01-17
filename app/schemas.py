from typing import Optional
from pydantic import BaseModel

from datetime import datetime

class LoginHistoryResponse(BaseModel):
    id: int
    user_id: int
    user_agent: str
    login_time: datetime

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True