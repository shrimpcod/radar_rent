from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List 

from app.db.session import get_db
from app.services.position_service import (
    get_position_by_id,
    get_positions,
    create_position,
    delete_position
)

from app.schemas.position import (
    PositionBase,
    PositionCreate,
    PositionResponse
)

from app.core.security import (
    get_current_active_user,
    get_current_agency_head, 
    get_current_superuser
)

from app.models.user import User

router = APIRouter()

@router.get("/{position_id}", response_model=PositionResponse)
async def get_position_endpoint(
    position_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить должность. Доступно всем авторизованным пользователям"""
    position = await get_position_by_id(db, position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Должность не найдена"
        )
    return position

@router.get("/", response_model=List[PositionResponse])
async def get_positions_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_agency_head)
):
    """Получить список должностей. Доступно суперадмину и руководителю агентства."""
    positions = await get_positions(db, skip=skip, limit=limit)
    return positions 

@router.post("/", response_model=PositionResponse, status_code=status.HTTP_201_CREATED)
async def create_position_endpoint(
    position_data: PositionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Создать должность. Доступно только суперадмину."""
    position = await create_position(db, position_data.model_dump())
    return position 

@router.delete("/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_position_endpoint(
    position_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Удалить должность. Доступно только суперадмину."""
    success = await delete_position(db, position_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Должность не найдена"
        )
    return None