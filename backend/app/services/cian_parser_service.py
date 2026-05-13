from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

from ..models.lead import Lead
from backend.workers.parsers.cian.parser import CianParser
from notifications.telegram.notifier import TelegramNotifier
from app.core.ws_manager import ws_manager
from app.schemas.lead import LeadResponse
from ..utils.delays import random_delay

class CianParserService: 
    """Сервис для парсинга объявлений Циан и созранения в БД"""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.parser = CianParser()
        self.notifier = TelegramNotifier()

    async def fetch_and_save_leads(self):
        """Получает объявления с Циан и сохраняет/обновляет их в БД"""
        await random_delay()

        print(f"[{datetime.now()}] Запуск парсера циан")\
        
        try:
            offers = await self.parser.fetch_listings()
            
            for offer in offers:
                await self._save_lead(offer)

            await self.db.commit()

        except Exception as e:
            await self.db.rollback()
            import traceback
            traceback.print_exc()
    
    async def _save_lead(self, offer: dict):
        parsed_data = self.parser.parse_offer(offer)
        cian_id = parsed_data["external_id"]

        if not parsed_data['published_offer_at']:
            return
        
        time_diff = datetime.now() - parsed_data['published_offer_at']
        is_fresh = time_diff <= timedelta(minutes=15)

        result = await self.db.execute(
            select(Lead).where(Lead.external_id == str(cian_id))
        )
        existing_url = result.scalar_one_or_none()

        if existing_url is None and is_fresh:
            await self._create_lead(parsed_data)

    async def _create_lead(self, data: dict): 
        lead = Lead(
            external_id=str(data["external_id"]),
            external_url=data['external_url'],
            price=data['price'],
            rooms_count=data['rooms_count'],
            area=data['area'],
            floor=data['floor'],
            floors_count=data['floors_count'],

            city=data['city'],
            metro_station=data['metro_station'],
            address=data['address'],

            #owner_offer_id=data['owner_id'],
            phone_number=data['phone_number'],

            created_offer_at=data['created_offer_at'],
            published_offer_at=data['published_offer_at'],

            is_early_access=data['is_early_access'],
            phone_reveal_at=data['phone_reveal_at'],
            source=data.get('source'),
            photo_urls=data.get('photos', []),
        )

        self.db.add(lead)
        await self.db.flush()
        lead_data = LeadResponse.model_validate(lead).model_dump(mode='json')
        await ws_manager.broadcast(lead_data)
        await self.notifier.send(lead)

        
