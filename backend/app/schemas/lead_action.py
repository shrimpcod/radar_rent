from datetime import datetime
from typing import Optional
from .base import BaseSchema


class LeadActionBase(BaseSchema):
    """Базовые поля действия по лиду."""
    
    user_id: int
    lead_id: int
    lead_status_id: Optional[int] = None
    call_id: Optional[int] = None
    is_favorite: bool = False
    last_action_time: datetime


class LeadActionCreate(LeadActionBase):
    """Схема для создания действия по лиду."""
    pass


class LeadActionUpdate(BaseSchema):
    """Схема для обновления действия по лиду.
    
    Все поля опциональные.
    """
    
    lead_status_id: Optional[int] = None
    call_id: Optional[int] = None
    is_favorite: Optional[bool] = None
    last_action_time: Optional[datetime] = None


class LeadActionResponse(LeadActionBase):
    """Схема для ответа API."""
    
    id: int
    
    class Config:
        from_attributes = True
