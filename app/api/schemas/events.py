from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    event_type: Optional[str] = None
    location: Optional[str] = None
    date: datetime
    deadline: Optional[datetime] = None
    max_seats: Optional[int] = None
    is_trending: Optional[bool] = False


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[str] = None
    location: Optional[str] = None
    date: Optional[datetime] = None
    deadline: Optional[datetime] = None
    max_seats: Optional[int] = None
    is_trending: Optional[bool] = None


class EventResponse(BaseModel):
    id: int
    club_id: int
    title: str
    description: Optional[str]
    event_type: Optional[str]
    location: Optional[str]
    date: datetime
    deadline: Optional[datetime]
    max_seats: Optional[int]
    current_registrations: int
    is_trending: bool
    view_count: int
    created_at: datetime
    updated_at: datetime


class DeleteResponse(BaseModel):
    success: bool
    message: str
    timestamp: datetime