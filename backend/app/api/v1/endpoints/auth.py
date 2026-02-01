from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.models.user import User
from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_login,
    authenticate_user,
)
from app.core.security import create_access_token, get_current_active_user
from app.core.config import settings

router = APIRouter()


def get_client_ip(request: Request) -> str:
    """Получает реальный ip-адрес клиента"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    return request.client.host


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user_data: UserCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Регистрация нового пользователя"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет прав доступа для регистрации"
        )

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
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Вход в систему c проверкой IP"""
    user = await authenticate_user(
        db,
        email=user_credentials.email_or_login,
        login=user_credentials.email_or_login,
        password=user_credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"}
        )

    current_ip = get_client_ip(request)
    if user.ip_address and user.ip_address != current_ip:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Доступ запрещен. Вход разрешен только с IP: {user.ip_address}"
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


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    """Выход из системы.

    В JWT-системе без blacklist токенов выход из системы
    реализуется на клиенте (удаление токена из localStorage).
    """
    return {"message": "Успешный выход из системы"}