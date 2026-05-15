from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.core.security import get_current_active_user
from app.schemas.favorite import FavoriteCreate, FavoriteResponse
from app.services.favorite_services import (
    get_user_favorites,
    add_to_favorites,
    remove_from_favorite
)

router = APIRouter()

@router.get("", response_model=List[FavoriteResponse])
async def read_favorites(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
): 
    return await get_user_favorites(db, current_user.id)

@router.post("", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
async def create_favorite(
    favorite_in: FavoriteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Добавить лид в избранное. (user_id берется из токена автоматически)"""
    return await add_to_favorites(db, user_id=current_user.id, lead_id=favorite_in.lead_id)

@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Удалить лид из избранного."""
    success = await remove_from_favorite(db, user_id=current_user.id, lead_id=lead_id)
    if not success:
        raise HTTPException(status_code=404, detail="Лид не найден в избранном")
    return None