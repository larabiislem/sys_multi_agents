from pydantic import BaseModel
from typing import Optional


class UserResponse(User):
    name: str
    email: str
    items: Optional[list[Item]] = None

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

    class Config:
        orm_mode = True