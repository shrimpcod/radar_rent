from fastapi import APIRouter, Depends 
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List 

from app.db.session import get_db
from app.models.user import User
from app.core.security import get_current_active_user
from app.services.lead_services import create_lead_action, get_current_user_lead_actions
from app.schemas.lead_action import LeadActionCreate, LeadActionResponse

router = APIRouter()

@router.get("", response_model=List[LeadActionResponse])
async def get_user_actions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить всю историю действий текущего пользователя."""
    return await get_current_user_lead_actions(db, current_user)

@router.post("/{lead_id}", response_model=LeadActionResponse)
async def post_action(
    action_in: LeadActionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Создать новую запись в журнале действий (Event Log).
    Вызывается, когда пользователь звонит, переходит по ссылке или меняет статус.
    """
    return await create_lead_action(
        db, 
        user_id=current_user.id,
        lead_id=action_in.lead_id,
        action_type=action_in.action_type,
        lead_status_id=action_in.lead_status_id, 
        call_id=action_in.call_id
    )