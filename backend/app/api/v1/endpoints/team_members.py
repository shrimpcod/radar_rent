from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from typing import List

from app.db.session import get_db
from app.services.team_member_service import (
    get_team_member_by_id, 
    get_team_members_by_team,
    create_team_member,
    update_team_member,
    delete_team_member,
) 

from app.services.team_service import get_team_by_id

from app.schemas.team_member import(
    TeamMemberBase, 
    TeamMemberCreate, 
    TeamMemberUpdate, 
    TeamMemberResponse
)

from app.core.security import (
    get_current_active_user
)

from app.models.team_member import TeamMember, TeamPosition
from app.models.user import User, UserType 
from app.models.team import Team

router = APIRouter()

async def check_team_member_acces(
        db: AsyncSession,
        member_id: int, 
        current_user: User,
) -> bool:
    if current_user.is_superuser:
        return True
    
    member = await get_team_member_by_id(db, member_id)
    if not member:
        return False 
    
    team = await get_team_by_id(db, member.team_id)
    if not team:
        return False 
    
    if current_user.agency_id == team.agency_id and current_user.user_type == UserType.SUPERVISOR:
        return True
    
    result = await db.execute(
        select(TeamMember)
        .where(
            TeamMember.team_id == team.id,
            TeamMember.user_id == current_user.id
        )
    )
    is_team_member = result.scalar_one_or_none()
    if is_team_member:
        return True
    
    return False

async def check_team_access(
        db: AsyncSession, 
        team_id: int, 
        current_user: User
) -> bool:
    """Проверить имеет ли доступ к команде"""
    if current_user.is_superuser:
        return True
    
    team = await get_team_by_id(db, team_id)
    if not team:
        return False
    
    if current_user.agency_id == team.agency_id and current_user.user_type == UserType.SUPERVISOR:
        return True
    
    result = await db.execute(
        select(TeamMember)
        .where(
            TeamMember.team_id == team_id,
            TeamMember.user_id == current_user.id
        )
    )
    is_team_member = result.scalar_one_or_none()
    if is_team_member:
        return True
    return False
    
@router.get("/{member_id}", response_model=TeamMemberResponse)
async def get_team_member_endpoint(
    member_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    """Получить участника команды по ID
    Доступно: самому участнику, руководителю агентства команды, супердамину"""
    
    member = await get_team_member_by_id(db, member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Участник команды не найден"
        )
    
    has_access = await check_team_member_acces(db, member_id, current_user)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому участнику команды"
        )
    
    return member 

@router.get("/", response_model=List[TeamMemberResponse])
async def get_team_members_endpoint(
    team_id: int,
    db: AsyncSession = Depends(get_db),
    skip: int = 0, 
    limit: int = 10, 
    current_user: User = Depends(get_current_active_user)
): 
    """Получить список участников команды
    Доступно: участникам команды, руководителю агентства команды, супердамину"""
    if not team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Необходимо указать айди команды"
        )
    
    team = await get_team_by_id(db, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Команда не найдена"
        )
    
    has_access = await check_team_access(db, team_id, current_user)

    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Нет доступа к списку сотрудников команды"
        )
    
    members = await get_team_members_by_team(db, team_id, skip=skip, limit=limit)
    return members 

@router.post("/", response_model=TeamMemberResponse, status_code=status.HTTP_201_CREATED)
async def create_team_member_endpoint(
    member_data: TeamMemberCreate,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
): 
    """Создать участника команды"""
    team = await get_team_by_id(db, member_data.team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Команда не найдена"
        )
    
    if not current_user.is_superuser: 
        if current_user.user_type != UserType.SUPERVISOR:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только руководитель агентсва может добавлять участников"
            )
        if team.agency_id != current_user.agency_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Можно добавлять участников только в команды своего агентсва"
            )
        
    member = await create_team_member(db, member_data.model_dump())
    return member

@router.put("/{member_id}", response_model=TeamMemberResponse)
async def update_team_member_endpoint(
    member_id: int, 
    member_data: TeamMemberUpdate,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
): 
    """Обновить участника команды"""
    member = await get_team_member_by_id(db, member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник команды не найден"
        )
    
    team = await get_team_by_id(db, member.team_id)
    if not team:
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Команда не найдена"
            )
    
    if not current_user.is_superuser:
        if team.agency_id != current_user.agency_id or current_user.user_type != UserType.SUPERVISOR:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Можно обновлять только участников команд своего агентства"
            )
        
    update_member = await update_team_member(db, member_id, member_data.model_dump(exclude_unset=True))
    return update_member 

@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team_member_endpoint(
    member_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
): 
    """Удалить участника команды"""
    member = await get_team_member_by_id(db, member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник команды не найден"
        ) 
    
    team = await get_team_by_id(db, member.team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Команда не найдена"
        )
    
    if not current_user.is_superuser:
        if team.agency_id != current_user.agency_id or current_user.user_type != UserType.SUPERVISOR:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Можно удалять только участников команд своего агентства"
            )
        
    success = await delete_team_member(db, member_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Участник команды не найден"
        )
    return None
