import asyncio
import logging
from sqlalchemy import select
from datetime import datetime

from app.db.session import AsyncSession, AsyncSessionLocal
from app.models.lead import Lead
from app.schemas.lead import LeadResponse
from app.core.ws_manager import ws_manager
from notifications.telegram.notifier import TelegramNotifier
from workers.queue_manager import queue_manager

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

async def process_lead(task_data: dict, db: AsyncSession) -> None:
    """Логика проверки на дубли и сохранения лида в БД"""
    external_id = str(task_data["external_id"])

    result = await db.execute(
        select(Lead)
        .where(Lead.external_id == external_id)
    )
    existing_lead = result.scalar_one_or_none()

    if existing_lead is None:
        logger.info(f"Сохраняем новый лид {external_id} в БД...")

        created_at_str = task_data.get("created_offer_at")
        published_at_str = task_data.get("published_offer_at")
        reveal_at_str = task_data.get("phone_reveal_at")

        created_at = datetime.fromisoformat(created_at_str) if created_at_str else datetime.now()
        published_at = datetime.fromisoformat(published_at_str) if published_at_str else None
        reveal_at = datetime.fromisoformat(reveal_at_str) if reveal_at_str else None

        new_lead = Lead(
            external_id = external_id,
            external_url = task_data.get("external_url"),
            price = task_data.get("price"),
            rooms_count = task_data.get("rooms_count"),
            area = task_data.get("area"),
            floor = task_data.get("floor"),
            floors_count = task_data.get("floors_count"),
            city = task_data.get("city"),
            metro_station=task_data.get("metro_station"),
            address = task_data.get("address"),
            phone_number = task_data.get("phone_number"),

            created_offer_at = created_at,
            published_offer_at = published_at,

            is_early_access = task_data.get("is_early_access", False),
            phone_reveal_at = reveal_at, 
            source = task_data.get("source"),
            photo_urls = task_data.get("photos", [])
        )

        db.add(new_lead)
        await db.commit()
        await db.refresh(new_lead)
        logger.info(f"Лид {external_id} успешно сохранен в БД!")

        try:
            lead_response = LeadResponse.model_validate(new_lead).model_dump(mode="json")
            await ws_manager.broadcast(lead_response)
            notifier = TelegramNotifier()
            await notifier.send(new_lead)
            logger.info(f"Уведомления по лиду {external_id} отправлены.")
        except Exception as e:
            logger.error(f"Ошибка отправки уведомлений по лиду {external_id}: {e}")
    else: 
        logger.info(f"Лид {external_id} уже существует в базе. Пропускаем.")
        

async def run_main_worker():
    """
       Консьюмер основной очереди. 
       Постоянно ждет новые задачи и обрабатывает их.
    """
    logger.info("Main Worker запущен. Ожидание задач...")
    
    try:
        while True:
            # Ждем задачу до 5 секунд (не нагружая процессор)
            task = await queue_manager.pop_from_main(timeout=5)
            
            if task:
                external_id = task.get("external_id", "Unknown")
                logger.info(f"Получена задача из Main Queue: Лид ID {external_id}")
                
                async with AsyncSessionLocal() as db:
                    try:
                        await process_lead(task, db)
                    except Exception as e:
                        logger.error(f"Ошибка при сохранении лида: {e}")
                        await db.rollback()

                
                logger.info(f"Лид ID {external_id} успешно обработан.")
                
    except asyncio.CancelledError:
        logger.info("Main Worker останавливается...")
    finally:
           await queue_manager.close()

if __name__ == "__main__":
    asyncio.run(run_main_worker())