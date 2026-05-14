from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.services.agency_service import (
    get_agency_by_id,
    get_agencies,
    create_agency,
    update_agency,
    delete_agency
)

from app.schemas.agency import (
    AgencyBase,
    AgencyCreate,
    AgencyUpdate,
    AgencyResponse
)

from app.core.security import (
    get_current_active_user, 
    get_current_superuser
)

from app.models.user import User

router = APIRouter()

@router.get("/{agency_id}", response_model=AgencyResponse)
async def get_agency_endpoint(
    agency_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    agency = await get_agency_by_id(db, agency_id)
    if not agency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Агентство не найдено"
        )

    return agency 

@router.get("/", response_model=List[AgencyResponse])
async def get_agencies_endpoint(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
): 
    """Получить список агентств. Доступно только суперадмину."""
    agencies = await get_agencies(db, skip=skip, limit=limit)
    return agencies

@router.post("/", response_model=AgencyResponse, status_code=status.HTTP_201_CREATED)
async def create_agency_endpoint(
    agency_data: AgencyCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
): 
    """Создать агентство. Доступно только суперадмину."""
    agency = await create_agency(db, agency_data.model_dump())
    return agency

@router.put("/{agency_id}", response_model=AgencyResponse)
async def update_agency_endpoint(
    agency_id: int, 
    agency_data: AgencyUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
): 
    """Обновить агентство. Доступно только суперадмину."""
    agency = await update_agency(
        db,
        agency_id, 
        agency_data.model_dump(exclude_unset=True)
    )
    if not agency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Агентство не найдено"
        )
    return agency

@router.delete("/{agency_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agency_endpoint(
    agency_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_superuser)
): 
    """Удалить агентство. Доступно только суперадмину."""
    success = await delete_agency(db, agency_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Агентство не найдено"
        )
    return None