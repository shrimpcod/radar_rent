import asyncio 
import logging

logger = logging.getLogger(__name__)

async def retry(func, max_attempts: int = 5, base_delay: float = 5.0):
    """
    Повторяет вызов func при ошибке.
    Задержки: 5 сек, 10 сек, 20 сек (каждый раз удваивается).
    """

    for attempt in range(1, max_attempts+1):
        try:
            return await func()
        except Exception as e:
            if attempt == max_attempts:
                logger.error(f"Все {max_attempts} попытки исчерпаны: {e}")
                raise
            delay = base_delay * (2 ** (attempt-1))
            logger.warning(f"Попытка {attempt} не удалась: {e}. Повтор через {delay} секунд..")
            await asyncio.sleep(delay)