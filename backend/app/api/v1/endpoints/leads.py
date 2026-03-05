from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ....db.session import get_db
from ....services.lead_services import get_leads

router = APIRouter()

@router.get("/leads")
async def get_all_leads(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
):
    leads = await get_leads(db, skip=skip, limit=limit)
    return{
        "total": len(leads),    
    }