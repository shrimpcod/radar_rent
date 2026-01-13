from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from ..core.config import settings

# Создание асинхронного движка
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Создание фабрики сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency для получения сессии БД
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session