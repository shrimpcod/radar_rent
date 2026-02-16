from fastapi import APIRouter
from app.api.v1.endpoints import auth, agencies, positions, teams, team_members, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(agencies.router, prefix="/agencies", tags=["agencies"])
api_router.include_router(positions.router, prefix="/positions", tags=["positions"])
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
api_router.include_router(team_members.router, prefix="/team_members", tags=["team-members"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
