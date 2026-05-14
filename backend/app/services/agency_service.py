from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select 
from app.models.agency import Agency 

async def get_agency_by_id(
        db: AsyncSession,
        agency_id: int
) -> Agency | None:
    result = await db.execute(select(Agency).where(Agency.id == agency_id))
    return result.scalar_one_or_none()

async def get_agencies(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
) -> list[Agency]:
    # Исправлено: нужно использовать scalars().all() для получения списка
    result = await db.execute(
        select(Agency)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_agency(
        db: AsyncSession,
        agency_data: dict
) -> Agency:
    db_agency = Agency(**agency_data)
    db.add(db_agency)
    await db.commit()
    await db.refresh(db_agency)
    return db_agency


async def update_agency(
        db: AsyncSession,
        agency_id: int,
        agency_data: dict
) -> Agency | None:
    """Обновить агентство.

    Args:
        db: Сессия базы данных
        agency_id: ID агентства
        agency_data: Данные для обновления (например, {"name": "Новое название"})

    Returns:
        Обновленное агентство или None если не найдено
    """
    agency = await get_agency_by_id(db, agency_id)
    if not agency:
        return None

    for key, value in agency_data.items():
        setattr(agency, key, value)

    await db.commit()
    await db.refresh(agency)
    return agency


async def delete_agency(
        db: AsyncSession,
        agency_id: int
) -> bool:
    """Удалить агентство по ID.

    Args:
        db: Сессия базы данных
        agency_id: ID агентства

    Returns:
        True если агентство удалено, False если не найдено
    """
    # Сначала получаем агентство
    agency = await get_agency_by_id(db, agency_id)
    if not agency:
        return False

    # Удаляем агентство
    await db.delete(agency)
    await db.commit()
    return True
