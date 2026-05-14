from typing import Optional
from .base import BaseSchema

class TeamBase(BaseSchema):
    """Базовые поля команды."""

    name: str
    agency_id: int


class TeamCreate(TeamBase):
    """Схема для создания команды."""
    pass


class TeamUpdate(BaseSchema):
    """Схема для обновления команды."""

    name: Optional[str] = None


class TeamResponse(TeamBase):
    """Схема для ответа API."""

    id: int

    class Config:
        from_attributes = True