import asyncio 
import logging 
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .parsers.cian.parser import CianParser
from .queue_manager import queue_manager
from .parsers.utils.delays import random_delay 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

async def fetch_and_queue_cian_leads():
    """Задача для шедулера: получает объявления с ЦИАН и отправляет в очереди Redis"""
    await random_delay()

    parser = CianParser()

    try: 
        offers = await parser.fetch_listings()

        for offer in offers: 
            parsed_data=parser.parse_offer(offer)

            if not parsed_data.get("published_offer_at"):
                continue

            time_diff = datetime.now() - parsed_data["published_offer_at"]
            is_fresh = time_diff <= timedelta(minutes=30)

            if is_fresh:
                external_id = parsed_data.get("external_id")
                is_early_access = parsed_data.get("is_early_access", False)
                reveal_time = parsed_data.get("phone_reveal_at")

                if is_early_access and reveal_time:
                    reveal_timestamp = int(reveal_time.timestamp())
                    await queue_manager.push_to_delayed(parsed_data, reveal_timestamp)
                    logger.info(f"Лид {external_id} отправлен в DELAYED очередь (повторный запрос в {reveal_time})")
                
                else: 
                    await queue_manager.push_to_main(parsed_data)
                    logger.info(f"Лид {external_id} отправлен в MAIN очередь")
    except Exception as e:
        logger.error(f"Ошибка при парсинге ЦИАН: {e}", exc_info=True)

async def start_parser_worker():
    """Запуск независимого воркера-парсера с планировщиком"""
    logger.info("Инициализация Parser Worker...")
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        fetch_and_queue_cian_leads,
        trigger=IntervalTrigger(minutes=30),
        id="cian_parser",
        name="Parser cian",
        replace_existing=True
    )

    scheduler.start()

    await fetch_and_queue_cian_leads()

    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        logger.info("Cian Parser Worker остановлен")

if __name__ == "__main__":
    asyncio.run(start_parser_worker())