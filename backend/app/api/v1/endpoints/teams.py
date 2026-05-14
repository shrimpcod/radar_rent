from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.services.team_service import (
    get_team_by_id,
    get_teams_by_agency,
    create_team,
    update_team,
    delete_team
)
from app.schemas.team import (
    TeamBase,
    TeamCreate,
    TeamUpdate,
    TeamResponse
)
from app.core.security import (
    get_current_active_user,
    get_current_superuser
)
from app.models.user import User, UserType
from app.models.team_member import TeamMember
from app.models.team import Team

router = APIRouter()


async def check_team_access(
    db: AsyncSession,
    team_id: int,
    current_user: User
) -> bool:
    """Проверить, имеет ли пользователь доступ к команде.

    Args:
        db: Сессия базы данных
        team_id: ID команды
        current_user: Текущий пользователь

    Returns:
        True если есть доступ, False в противном случае
    """
    # Суперадмин имеет доступ ко всем командам
    if current_user.is_superuser:
        return True

    # Получаем команду
    team = await get_team_by_id(db, team_id)
    if not team:
        return False

    # Руководитель агентства имеет доступ к командам своего агентства
    if current_user.agency_id == team.agency_id and current_user.user_type == UserType.SUPERVISOR: 
        return True

    # Проверяем, является ли пользователь членом команды
    result = await db.execute(
        select(TeamMember).where(
            TeamMember.team_id == team_id,
            TeamMember.user_id == current_user.id
        )
    )
    team_member = result.scalar_one_or_none()
    if team_member:
        return True

    return False


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team_endpoint(
    team_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить команду по ID.
    Доступно: члену команды, руководителю агентства команды, суперадмину."""
    team = await get_team_by_id(db, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Команда не найдена"
        )

    # Проверяем доступ
    has_access = await check_team_access(db, team_id, current_user)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этой команде"
        )

    return team


@router.get("/", response_model=List[TeamResponse])
async def get_teams_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить список команд.
    Суперадмин видит все команды.
    Руководитель агентства видит команды своего агентства."""
    # Суперадмин видит все команды (через agency_id=None для всех)
    if current_user.is_superuser:
        # Получаем все команды через специальный запрос
        result = await db.execute(
            select(Team).offset(skip).limit(limit)
        )
        return result.scalars().all()

    # Руководитель агентства видит только команды своего агентства
    if current_user.agency_id and current_user.user_type == UserType.SUPERVISOR:
        teams = await get_teams_by_agency(
            db,
            current_user.agency_id,
            skip=skip,
            limit=limit
        )
        return teams

    # Обычный пользователь не может видеть список команд
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Нет доступа к списку команд"
    )


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team_endpoint(
    team_data: TeamCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Создать команду.
    Суперадмин может создать команду для любого агентства.
    Руководитель агентства может создать команду только для своего агентства."""
    # Суперадмин может создавать команды для любого агентства
    if not current_user.is_superuser:
        # Проверяем, что пользователь является руководителем агентства
        if current_user.user_type != UserType.SUPERVISOR:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только руководитель агентства может создавать команды"
            )
        # Руководитель может создавать команды только для своего агентства
        if team_data.agency_id != current_user.agency_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Можно создавать команды только для своего агентства"
            )

    team = await create_team(db, team_data.model_dump())
    return team


@router.put("/{team_id}", response_model=TeamResponse)
async def update_team_endpoint(
    team_id: int,
    team_data: TeamUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Обновить команду.
    Суперадмин может обновить любую команду.
    Руководитель агентства может обновлять только команды своего агентства."""
    # Получаем команду
    team = await get_team_by_id(db, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Команда не найдена"
        )

    # Суперадмин может обновлять любую команду
    if not current_user.is_superuser:
        # Проверяем, что команда принадлежит агентству пользователя
        if team.agency_id != current_user.agency_id or current_user.user_type != UserType.SUPERVISOR:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Можно обновлять только команды своего агентства"
            )

    updated_team = await update_team(
        db,
        team_id,
        team_data.model_dump(exclude_unset=True)
    )
    return updated_team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team_endpoint(
    team_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Удалить команду.
    Суперадмин может удалить любую команду.
    Руководитель агентства может удалять только команды своего агентства."""
    # Получаем команду
    team = await get_team_by_id(db, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Команда не найдена"
        )

    # Суперадмин может удалять любую команду
    if not current_user.is_superuser:
        # Проверяем, что команда принадлежит агентству пользователя
        if team.agency_id != current_user.agency_id or current_user.user_type != UserType.SUPERVISOR:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Можно удалять только команды своего агентства"
            )

    success = await delete_team(db, team_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Команда не найдена"
        )
    return None
