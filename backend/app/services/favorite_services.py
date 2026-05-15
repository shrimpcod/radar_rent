from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.favorite import Favorite
from typing import List, Optional

async def get_user_favorites(db: AsyncSession, user_id: int) -> List[Favorite]: 
    """Получить список всех избранных лидов пользователя."""
    result = await db.execute(
        select(Favorite).where(Favorite.user_id == user_id)
    )
    return result.scalars().all()

async def get_favorites_by_lead(
        db: AsyncSession,
        user_id: int, 
        lead_id: int, 
) -> Optional[Favorite]: 
    """Проверить, есть ли конкретный лид в избранном у пользователя."""
    result = await db.execute(
        select(Favorite).where(
            and_(Favorite.user_id == user_id, Favorite.lead_id == lead_id)
        )
    )
    return result.scalar_one_or_none()
    
async def add_to_favorites(
        db: AsyncSession,
        user_id: int,
        lead_id: int,
) -> Favorite:
    """Добавить лид в избранное."""
    existing = await get_favorites_by_lead(db, user_id, lead_id)
    if existing:
        return existing
    
    favorite = Favorite(
        user_id=user_id,
        lead_id=lead_id
    )

    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite

async def remove_from_favorite(
        db: AsyncSession,
        user_id: int,
        lead_id: int,
) -> bool:
    """Удалить лид из избранного."""
    favorite = await get_favorites_by_lead(db, user_id, lead_id)
    if not favorite:
        return False
    
    await db.delete(favorite)
    await db.commit()
    return True
