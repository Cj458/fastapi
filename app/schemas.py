from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str


class UserCreate(UserBase):
    pass


class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True   
