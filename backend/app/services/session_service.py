from datetime import datetime, date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_ 
from app.models.user_session import UserSession 

async def track_user_activity(db: AsyncSession, user_id: int):
    today = date.today()
    now = datetime.now()

    result = await db.execute(
        select(UserSession)
        .where(
            and_(UserSession.user_id == user_id, UserSession.session_date == today)
        )
    )
    session = result.scalars().first()

    if not session:
        new_session = UserSession(
            user_id=user_id,
            session_date = today,
            login_at=now,
            logout_at=now,
            time_in_the_system=datetime(1970, 1, 1, 0, 0, 0)
        )
        db.add(new_session)
        await db.commit()
    else:
        session.logout_at = now

        time_diff = now - session.login_at

        base_date = datetime(1970, 1, 1)
        session.time_in_the_system = base_date + time_diff

        db.add(session)
        await db.commit()
