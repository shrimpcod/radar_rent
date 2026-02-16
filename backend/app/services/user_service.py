from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.user import User
from ..models.agency import Agency
from ..models.position import Position
from ..core.security import get_password_hash, verify_password
from typing import Optional

async def get_user_by_email(
        db: AsyncSession,
        email: str 
) -> User | None: 
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_login(
        db: AsyncSession,
        login: str
) -> User | None:
    result = await db.execute(select(User).where(User.login == login))
    return result.scalar_one_or_none()

async def get_user_by_id(
        db: AsyncSession,
        user_id: int
) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def create_user(
        db: AsyncSession,
        user_data: dict
) -> User: 
    hashed_password = get_password_hash(user_data["password"])
    del user_data["password"]

    user_data["hashed_password"] = hashed_password

    db_user = User(**user_data)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def authenticate_user(
        db: AsyncSession,
        email: Optional[str],
        login: Optional[str],
        password: str
) -> Optional[User]:
    user = await get_user_by_email(db, email)
    if not user:
        user = await get_user_by_login(db, login)

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def update_user(
        db: AsyncSession,
        user_id: int,
        user_data: dict
) -> User | None:
    """Обновить пользователя.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя
        user_data: Данные для обновления (например, {"name": "Новое имя"})

    Returns:
        Обновленный пользователь или None если не найден
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    # Проверяем, что agency_id существует, если он указан
    if "agency_id" in user_data and user_data["agency_id"] is not None:
        agency = await db.execute(select(Agency).where(Agency.id == user_data["agency_id"]))
        if not agency.scalar_one_or_none():
            raise ValueError(f"Agency with id {user_data['agency_id']} does not exist")

    # Проверяем, что position_id существует, если он указан
    if "position_id" in user_data and user_data["position_id"] is not None:
        position = await db.execute(select(Position).where(Position.id == user_data["position_id"]))
        if not position.scalar_one_or_none():
            raise ValueError(f"Position with id {user_data['position_id']} does not exist")

    # Обновляем поля
    for key, value in user_data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(
        db: AsyncSession,
        user_id: int
) -> bool:
    """Удалить пользователя по ID.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя

    Returns:
        True если пользователь удален, False если не найден
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return False

    await db.delete(user)
    await db.commit()
    return True
