from typing import Optional
from .base import BaseSchema


class PositionBase(BaseSchema):
    """Базовые поля должности."""
    
    name: str


class PositionCreate(PositionBase):
    """Схема для создания должности."""
    pass


class PositionUpdate(BaseSchema):
    """Схема для обновления должности."""
    
    name: Optional[str] = None


class PositionResponse(PositionBase):
    """Схема для ответа API."""
    
    id: int
    
    class Config:
        from_attributes = True
