from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ..models.lead import Lead
from ..core.security import get_password_hash, verify_password
from typing import Optional, List
from datetime import datetime, timezone
from ..models.lead_action import LeadAction
from ..models.user import User


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

async def get_leads_count(db: AsyncSession) -> int:
    result = await db.execute(select(func.count()).select_from(Lead))
    return result.scalar()

async def get_current_user_lead_actions(
    db: AsyncSession,
    current_user: User,    
):
    result = await db.execute(
        select(LeadAction).where(LeadAction.user_id == current_user.id)
    )
    return result.scalars().all()
    
async def get_lead_action(
        db: AsyncSession, 
        user_id: int,
        lead_id: int
) -> Optional[LeadAction]:
    result = await db.execute(
        select(LeadAction)
        .where(LeadAction.user_id == user_id, LeadAction.lead_id == lead_id)
    )
    return result.scalar_one_or_none()

async def upsert_lead_action(
        db: AsyncSession,
        user_id: int,
        lead_id: int, 
        is_favorite: Optional[bool] = None,
        lead_status_id: Optional[int] = None
) -> LeadAction:
    action = await get_lead_action(db, user_id, lead_id)

    if action is None:
        action = LeadAction(
            user_id=user_id,
            lead_id=lead_id,
            is_favorite=is_favorite if is_favorite is not None else False,
            lead_status_id=lead_status_id,
            last_action_time = datetime.utcnow()
        )
        db.add(action)
    else:
        if is_favorite is not None:
            action.is_favorite = is_favorite
        if lead_status_id is not None:
            action.lead_status_id = lead_status_id
        action.last_action_time = datetime.utcnow()

    await db.commit()
    await db.refresh(action)
    return action 

