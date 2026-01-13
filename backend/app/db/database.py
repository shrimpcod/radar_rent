from sqlalchemy.ext.asyncio import AsyncEngine
from ..models.base import Base
from .session import engine

# Функция для создания всех таблиц
async def init_db():
    """Создание всех таблиц в базе данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Функция для удаления всех таблиц (только для тестов)
async def drop_db():
    """Удаление всех таблиц из базы данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
