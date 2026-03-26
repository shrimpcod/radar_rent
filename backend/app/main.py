from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.core.config import settings
from app.db.session import get_db
from app.services.cian_parser_service import CianParserService

from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

scheduler = AsyncIOScheduler()
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    
    async def parse_cian_taks():
        async for db in get_db():
            service = CianParserService(db)
            await service.fetch_and_save_leads()
            break
    
    scheduler.add_job(
       parse_cian_taks,
       trigger=IntervalTrigger(minutes=5, jitter=60),
       id='cian_parser',
       name='Parser cian',
       replace_existing=True
    )

    await parse_cian_taks()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Корневой endpoint для проверки работы сервера"""
    return{
        "message": "Radar Rent API",
        "version": "0.1.0",
        "docs": "/api/docs"
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "ok"}