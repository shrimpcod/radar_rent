from datetime import datetime
from typing import Optional
from .base import BaseSchema
from app.models.lead_action import ActionType


class LeadActionBase(BaseSchema):
    """Базовые поля действия по лиду."""
    
    user_id: int
    lead_id: int
    lead_status_id: Optional[int] = None
    call_id: Optional[int] = None
    action_type: ActionType
    action_date: datetime


class LeadActionCreate(LeadActionBase):
    """Схема для создания действия по лиду."""
    pass


class LeadActionUpdate(BaseSchema):
    """Схема для обновления действия по лиду.
    
    Все поля опциональные.
    """
    lead_status_id: Optional[int] = None
    call_id: Optional[int] = None
    action_type: Optional[ActionType] = None
    action_date: Optional[datetime] = None 


class LeadActionResponse(LeadActionBase):
    """Схема для ответа API."""
    
    id: int
    
    class Config:
        from_attributes = True
