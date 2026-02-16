from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.services.user_service import (
    get_user_by_id,
    get_user_by_email,
    create_user,
    update_user,
    delete_user
)
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse
)
from app.core.security import get_current_active_user
from app.models.user import User, UserType

router = APIRouter()


async def check_user_access(
    db: AsyncSession,
    user_id: int,
    current_user: User
) -> bool:
    """Проверить, имеет ли пользователь доступ к другому пользователю."""
    # Суперадмин имеет доступ ко всем пользователям
    if current_user.is_superuser:
        return True

    # Получаем пользователя
    user = await get_user_by_id(db, user_id)
    if not user:
        return False

    # Руководитель агентства имеет доступ к сотрудникам своего агентства
    if current_user.agency_id and current_user.user_type == UserType.SUPERVISOR:
        if user.agency_id == current_user.agency_id:
            return True

    return False


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить пользователя по ID.
    Суперадмин видит всех пользователей.
    Руководитель агентства видит сотрудников своего агентства."""
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    has_access = await check_user_access(db, user_id, current_user)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому пользователю"
        )

    return user


@router.get("/", response_model=List[UserResponse])
async def get_users_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить список пользователей.
    Суперадмин видит всех пользователей.
    Руководитель агентства видит сотрудников своего агентства."""
    # Суперадмин видит всех пользователей
    if current_user.is_superuser:
        result = await db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()

    # Руководитель агентства видит только сотрудников своего агентства
    if current_user.agency_id and current_user.user_type == UserType.SUPERVISOR:
        result = await db.execute(
            select(User)
            .where(User.agency_id == current_user.agency_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    # Обычный пользователь не может видеть список пользователей
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Нет доступа к списку пользователей"
    )


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Создать пользователя.
    Суперадмин может создать любого пользователя.
    Руководитель агентства может создать только сотрудника своего агентства."""
    # Суперадмин может создавать пользователей для любого агентства
    if not current_user.is_superuser:
        # Проверяем, что пользователь является руководителем агентства
        if current_user.user_type != UserType.SUPERVISOR:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Только руководитель агентства может создавать пользователей"
            )
        # Руководитель может создавать сотрудников только для своего агентства
        if user_data.agency_id != current_user.agency_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Можно создавать сотрудников только для своего агентства"
            )

    # Проверяем, что email не занят
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )

    user = await create_user(db, user_data.model_dump())
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user_endpoint(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Обновить пользователя.
    Суперадмин может обновить любого пользователя.
    Руководитель агентства может обновлять только сотрудников своего агентства."""
    has_access = await check_user_access(db, user_id, current_user)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому пользователю"
        )

    try:
        updated_user = await update_user(
            db,
            user_id,
            user_data.model_dump(exclude_unset=True)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Удалить пользователя.
    Только суперадмин может удалять пользователей."""
    # Только суперадмин может удалять пользователей
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только суперадмин может удалять пользователей"
        )

    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    return None
