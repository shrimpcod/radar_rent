from fastapi import APIRouter, Depends 
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List 

from ....db.session import get_db
from ....models.user import User
from ....core.security import get_current_active_user
from ....services.lead_services import get_lead_action, upsert_lead_action, get_current_user_lead_actions
from ....schemas.lead_action import LeadActionResponse

router = APIRouter()

@router.get("", response_model=List[LeadActionResponse])
async def get_user_actions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await get_current_user_lead_actions(db, current_user)


@router.get("/{lead_id}", response_model=LeadActionResponse | None)
async def get_action(
    lead_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
): 
    return await get_lead_action(db, user_id=current_user.id, lead_id=lead_id)

@router.patch("/{lead_id}", response_model=LeadActionResponse)
async def patch_action(
    lead_id: int, 
    is_favorite: Optional[bool] = None, 
    lead_status_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await upsert_lead_action(
        db, 
        user_id=current_user.id,
        lead_id=lead_id,
        is_favorite=is_favorite,
        lead_status_id=lead_status_id
    )