from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.position import Position

async def get_position_by_id(
        db: AsyncSession, 
        position_id: int
) -> Position | None:
    result = await db.execute(select(Position).where(Position.id == position_id))
    return result.scalar_one_or_none()

async def get_positions(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
) -> list[Position]:
    result = await db.execute(
        select(Position)
        .offset(skip)
        .limit(limit)    
    )
    return result.scalars().all()

async def create_position(
        db:  AsyncSession,
        position_data: dict
) -> Position:
    db_position = Position(**position_data)
    # Ошибка: нужно добавлять db_position, а не position_data
    db.add(db_position)
    await db.commit()
    await db.refresh(db_position)
    return db_position


async def update_position(
        db: AsyncSession,
        position_id: int,
        position_data: dict
) -> Position | None:
    """Обновить должность.

    Args:
        db: Сессия базы данных
        position_id: ID должности
        position_data: Данные для обновления (например, {"name": "Новое название"})

    Returns:
        Обновленная должность или None если не найдена
    """
    # Сначала получаем должность
    position = await get_position_by_id(db, position_id)
    if not position:
        return None

    # Обновляем поля
    for key, value in position_data.items():
        setattr(position, key, value)

    await db.commit()
    await db.refresh(position)
    return position

async def delete_position(
        db: AsyncSession, 
        position_id: int
) -> bool:
    position = await get_position_by_id(db, position_id)
    if not position:
        return False
    await db.delete(position)
    await db.commit()
    return True
    