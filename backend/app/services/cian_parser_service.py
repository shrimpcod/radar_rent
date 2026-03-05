from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

from ..models.lead import Lead
from cian_parser_api.parser import CianParser
from telegram_bot.bot.bot import send_lead_to_tg

class CianParserService: 
    """Сервис для парсинга объявлений Циан и созранения в БД"""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.parser = CianParser()

    async def fetch_and_save_leads(self):
        """Получает объявления с Циан и сохраняет/обновляет их в БД"""

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
        cian_id = parsed_data["cian_id"]

        if not parsed_data['published_at']:
            return
        
        time_diff = datetime.now() - parsed_data['published_at']
        is_fresh = time_diff <= timedelta(minutes=15)

        result = await self.db.execute(
            select(Lead).where(Lead.external_id == str(cian_id))
        )
        existing_url = result.scalar_one_or_none()

        if existing_url is None and is_fresh:
            await self._create_lead(parsed_data)

    async def _create_lead(self, data: dict): 
        lead = Lead(
            external_id=str(data["cian_id"]),
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

            created_offer_at=data['created_at'],
            published_offer_at=data['published_at'],

            is_early_access=data['is_early_access'],
            phone_reveal_at=data['phone_reveal_at'],
        )

        self.db.add(lead)
        await send_lead_to_tg(lead)

        
