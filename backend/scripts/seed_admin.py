import asyncio
import sys
from pathlib import Path

# Добавляем директорию backend в PYTHONPATH
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash 

async def create_superuser():
    """Создаем суперадмина"""
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(User).where((User.email == "admin@radarrent.ru") & (User.is_superuser == True))
        )
        existing_admin = result.scalar_one_or_none()

        if existing_admin:
            print("Суперадмин уже существует!")
            print(f"Email: {existing_admin.email}")
            print(f"Login: {existing_admin.login}")
            return

        admin = User(
            email="admin@radarrent.ru",
            login="adminRR",
            fullname="Суперадмин",
            hashed_password=get_password_hash("AdminRR"),
            ip_address=None,
            is_active=True,
            is_superuser=True
        )

        session.add(admin)
        await session.commit()
        await session.refresh(admin)

        print("Суперадмин успешно создан!")
        print(f"    ID: {admin.id}")
        print(f"    Email: {admin.email}")
        print(f"    Login: {admin.login}")
        print(f"    Пароль: AdminRR")
        print(f"    IP: {admin.ip_address} (может входить с любого IP)")

if __name__ == "__main__":
    asyncio.run(create_superuser())
