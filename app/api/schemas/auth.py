from pydantic import BaseModel
from typing import Optional


from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class StudentLogin(BaseModel):
    email: EmailStr
    password: str


class ClubLogin(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    success: bool
    message: str
    user_type: str
    user_id: int
    name: str
    email: str
    timestamp: datetime


class StudentRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    field_of_study: Optional[str] = None
    year_level: Optional[int] = None


class ClubRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    description: Optional[str] = None
    mission: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    website: Optional[str] = None
    personality_style: Optional[str] = "friendly"


class RegisterResponse(BaseModel):
    success: bool
    message: str
    user_id: int
    timestamp: datetime


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    timestamp: datetime
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

    class Config:
        orm_mode = True