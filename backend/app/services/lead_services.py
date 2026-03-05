from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.lead import Lead
from ..core.security import get_password_hash, verify_password
from typing import Optional, List

async def get_leads(
        db: AsyncSession, 
        skip: int = 0,
        limit: int = 100
) -> List[Lead]: 
    result = await db.execute(
        select(Lead)
        .order_by(Lead.published_offer_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()