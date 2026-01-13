from typing import Optional
from .base import BaseSchema


class AgencyBase(BaseSchema):
    """Базовые поля агентства."""
    
    name: str


class AgencyCreate(AgencyBase):
    """Схема для создания агентства."""
    pass


class AgencyUpdate(BaseSchema):
    """Схема для обновления агентства."""
    
    name: Optional[str] = None


class AgencyResponse(AgencyBase):
    """Схема для ответа API."""
    
    id: int
    
    class Config:
        from_attributes = True
