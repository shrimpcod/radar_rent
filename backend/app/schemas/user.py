from pydantic import EmailStr, Field, field_validator
from typing import Optional, Union
from .base import BaseSchema
from app.models.user import UserType


class UserBase(BaseSchema):
    """Базовые поля пользователя."""
    email: EmailStr
    login: str
    fullname: str
    user_type: UserType = UserType.PRIVATE
    ip_address: str
    agency_id: Optional[int] = None
    position_id: Optional[int] = None


class UserCreate(UserBase):
    """Схема для создания пользователя.
    Включает пароль, который будет хеширован перед сохранением в БД.
    """
    
    password: str = Field(..., min_length=6, max_length=18)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Валидация пароля."""
        if not any(char.isdigit() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        if not any(char.isupper() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not any(char.islower() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
        return v


class UserUpdate(BaseSchema):
    """Схема для обновления пользователя.
    Все поля опциональные, пароль не включается (отдельный endpoint для смены пароля).
    """
    
    email: Optional[EmailStr] = None
    login: Optional[str] = None
    fullname: Optional[str] = None
    user_type: Optional[UserType] = None
    ip_address: Optional[str] = None
    agency_id: Optional[int] = None
    position_id: Optional[int] = None


class UserResponse(UserBase):
    """Схема для ответа API.
    Включает ID пользователя, но НЕ включает пароль.
    """
    
    id: int
    
    class Config:
        from_attributes = True


class UserLogin(BaseSchema):
    """Схема для входа пользователя.
    Используется для аутентификации.
    """
    
    login_or_email: Union[str, EmailStr] 
    password: str


class UserChangePassword(BaseSchema):
    """Схема для смены пароля."""
    
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v):
        """Валидация нового пароля."""
        if not any(char.isdigit() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        if not any(char.isupper() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not any(char.islower() for char in v):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
        return v
