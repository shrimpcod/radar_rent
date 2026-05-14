from typing import Optional
from pydantic import Field, field_validator
from .base import BaseSchema


class LeadStatusBase(BaseSchema):
    """Базовые поля статуса лида."""
    
    name: str = Field(..., min_length=1, description="Название статуса")
    color: str = Field(..., pattern=r'^#[0-9A-Fa-f]{6}$', description="Цвет в формате HEX (#RRGGBB)")
    
    @field_validator('color')
    @classmethod
    def validate_color(cls, v):
        """Валидация цвета."""
        if not v.startswith('#'):
            raise ValueError('Цвет должен начинаться с #')
        if len(v) != 7:
            raise ValueError('Цвет должен быть в формате #RRGGBB')
        return v


class LeadStatusCreate(LeadStatusBase):
    """Схема для создания статуса лида."""
    pass


class LeadStatusUpdate(BaseSchema):
    """Схема для обновления статуса лида."""
    
    name: Optional[str] = Field(None, min_length=1)
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')


class LeadStatusResponse(LeadStatusBase):
    """Схема для ответа API."""
    
    id: int
    
    class Config:
        from_attributes = True
