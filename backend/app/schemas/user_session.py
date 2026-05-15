from datetime import date, datetime
from typing import Optional
from .base import BaseSchema

class UserSessionBase(BaseSchema):
    user_id: int
    session_date: date
    login_at: datetime
    logout_at: Optional[datetime] = None
    time_in_the_system: Optional[datetime] = None

class UserSessionCreate(UserSessionBase):
    pass

class UserSessionUpdate(UserSessionBase):
    logout_at: Optional[datetime] = None
    time_in_the_system: Optional[datetime] = None

class UserSessionResponse(UserSessionBase):
    id: int

    class Config:
        from_attributes = True