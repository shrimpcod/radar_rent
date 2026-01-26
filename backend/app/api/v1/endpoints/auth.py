from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession 
from datetime import timedelta

from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_login, 
    authenticate_user,
)   
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Регистрация нового пользователя"""
    existing_email = await get_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )
    
    existing_login = await get_user_by_login(db, user_data.login)
    if existing_login:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином уже существует"
        )
    user_dict = user_data.model_dump()
    user = await create_user(db, user_dict)

    return user

@router.post("/login")
async def login(
    user_credentials: UserLogin, 
    db: AsyncSession = Depends(get_db)   
):
    """Вход в систему"""
    user = await authenticate_user(
        db,
        email_or_login = user_credentials.email_or_login,
        password = user_credentials.password 
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expire
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }