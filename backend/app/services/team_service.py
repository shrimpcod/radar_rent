from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.team import Team 

async def get_team_by_id(
        db: AsyncSession, 
        team_id: int 
) -> Team | None:
    result = await db.execute(select(Team).where(Team.id == team_id))
    return result.scalar_one_or_none()

async def get_teams_by_agency(
        db: AsyncSession, 
        agency_id: int, 
        skip: int = 0,
        limit: int = 100
) -> list[Team]:
    result = await db.execute(
        select(Team)
        .where(Team.agency_id == agency_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_team(
        db: AsyncSession, 
        team_data: dict
) -> Team:
    db_team = Team(**team_data)
    db.add(db_team)
    await db.commit()
    await db.refresh(db_team)
    return db_team

async def update_team(
        db: AsyncSession, 
        team_id: int, 
        team_data: dict
) -> Team | None: 
    team = await get_team_by_id(db, team_id)
    if not team:
        return None

    for key, value in team_data.items():
        setattr(team, key, value)

    await db.commit()
    await db.refresh(team)
    return team

async def delete_team(
        db: AsyncSession,
        team_id: int
) -> bool:
    team = await get_team_by_id(db, team_id)
    if not team:
        return False

    await db.delete(team)
    await db.commit()
    return True