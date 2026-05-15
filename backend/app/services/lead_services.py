from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.lead import Lead
from typing import Optional, List
from datetime import datetime
from app.models.lead_action import LeadAction
from app.models.lead_action import ActionType
from app.models.user import User


async def get_leads(
        db: AsyncSession, 
        skip: int = 0,
        limit: int = 100
) -> List[Lead]: 
    """
        Функция отдает записи из бд при первичной загрузке страницы
    """
    result = await db.execute(
        select(Lead)
        .order_by(Lead.published_offer_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_leads_count(db: AsyncSession) -> int:
    """
        Функция для пагинации на фронтенде
    """
    result = await db.execute(select(func.count()).select_from(Lead))
    return result.scalar()

async def get_current_user_lead_actions(
    db: AsyncSession,
    current_user: User,    
):
    """
        Функция для личной статистики пользователя
    """
    result = await db.execute(
        select(LeadAction).where(LeadAction.user_id == current_user.id)
    )
    return result.scalars().all()

async def create_lead_action(
        db: AsyncSession,
        user_id: int,
        lead_id: int, 
        action_type: ActionType,
        lead_status_id: Optional[int] = None,
        call_id: Optional[int] = None,
) -> LeadAction:
    action = LeadAction(
        user_id=user_id,
        lead_id=lead_id,
        action_type=action_type,
        lead_status_id=lead_status_id,
        call_id=call_id,
        action_date=datetime.now()
    )
    db.add(action)
    await db.commit()
    await db.refresh(action)
    return action



