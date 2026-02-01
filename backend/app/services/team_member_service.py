from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from app.models.team_member import TeamMember 

async def get_team_member_by_id(
        db: AsyncSession,
        team_member_id: int
) -> TeamMember | None: 
    result = await db.execute(select(TeamMember).where(TeamMember.id == team_member_id))
    return result.scalar_one_or_none()

async def get_team_members_by_team(
        db: AsyncSession, 
        team_id: int, 
        skip: int = 0, 
        limit: int = 100
) -> list[TeamMember]: 
    result = await db.execute(
        select(TeamMember)
        .where(TeamMember.team_id == team_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_team_member(
        db: AsyncSession,
        member_data: dict
) -> TeamMember: 
    db_team_member = TeamMember(**member_data)
    db.add(db_team_member)
    await db.commit()
    await db.refresh(db_team_member)
    return db_team_member

async def update_team_member(
        db: AsyncSession, 
        member_id: int,
        member_data: dict
) -> TeamMember | None: 
    member = await get_team_member_by_id(db, member_id)
    if not member:
        return None
    
    for key, value in member_data.items():
        setattr(member, key, value)

    await db.commit()
    await db.refresh(member)

    return member 

async def delete_team_member(
        db: AsyncSession, 
        member_id: int
) -> bool:
    member = await get_team_member_by_id(db, member_id)
    if not member:
        return False
    
    await db.delete(member)
    await db.commit()
    return True
