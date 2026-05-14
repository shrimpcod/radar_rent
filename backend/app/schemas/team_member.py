from typing import Optional
from .base import BaseSchema
from app.models.team_member import TeamPosition


class TeamMemberBase(BaseSchema):
    """Базовые поля участника команды."""

    team_id: int
    user_id: int
    team_position: TeamPosition = TeamPosition.MEMBER


class TeamMemberCreate(TeamMemberBase):
    """Схема для добавления участника в команду."""
    pass


class TeamMemberUpdate(BaseSchema):
    """Схема для обновления роли участника."""

    team_position: Optional[TeamPosition] = None


class TeamMemberResponse(TeamMemberBase):
    """Схема для ответа API."""

    id: int

    class Config:
        from_attributes = True
