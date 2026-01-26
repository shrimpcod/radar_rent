from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.user import User
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
        email_or_login: Optional[str],
        password: str
) -> Optional[User]: 
    user = await get_user_by_email(db, email_or_login)
    if not user:
        user = await get_user_by_login(db, email_or_login)

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
