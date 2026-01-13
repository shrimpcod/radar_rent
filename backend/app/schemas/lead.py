from datetime import datetime
from typing import Optional
from pydantic import Field, field_validator
from .base import BaseSchema


class LeadBase(BaseSchema):
    """Базовые поля лида."""
    
    rooms_count: int = Field(..., gt=0, description="Количество комнат")
    city: str = Field(..., min_length=1, description="Город")
    metro_station: Optional[str] = Field(None, description="Станция метро")
    area: float = Field(..., gt=0, description="Площадь в кв.м")
    floor: int = Field(..., gt=0, description="Этаж")
    price: float = Field(..., gt=0, description="Цена")
    address: str = Field(..., min_length=1, description="Полный адрес")
    phone_number: str = Field(..., min_length=10, description="Номер телефона")
    owner_id: int = Field(..., description="ID собственника")
    notes: Optional[str] = Field(None, description="Заметки")
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v):
        """Валидация номера телефона."""
        # Убираем все символы кроме цифр
        cleaned = ''.join(filter(str.isdigit, v))
        if len(cleaned) < 10:
            raise ValueError('Номер телефона должен содержать минимум 10 цифр')
        return v


class LeadCreate(LeadBase):
    """Схема для создания лида.
    
    Дата создания будет установлена автоматически.
    """
    pass


class LeadUpdate(BaseSchema):
    """Схема для обновления лида.
    
    Все поля опциональные.
    """
    
    rooms_count: Optional[int] = Field(None, gt=0)
    city: Optional[str] = Field(None, min_length=1)
    metro_station: Optional[str] = None
    area: Optional[float] = Field(None, gt=0)
    floor: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    address: Optional[str] = Field(None, min_length=1)
    phone_number: Optional[str] = Field(None, min_length=10)
    owner_id: Optional[int] = None
    notes: Optional[str] = None


class LeadResponse(LeadBase):
    """Схема для ответа API."""
    
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
