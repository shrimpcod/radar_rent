from fastapi import APIRouter
from app.api.v1.endpoints import auth

api_router = APIRouter()
api_router.inclide_router(auth.router, prefix="/auth", tags=["auth"])
