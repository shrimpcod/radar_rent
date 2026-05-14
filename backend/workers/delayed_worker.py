import asyncio
import logging
from workers.queue_manager import queue_manager

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Интервал проверки отложенной очереди (в секундах)
CHECK_INTERVAL = 15 

async def run_delayed_worker():
    """
    Специализированный процесс для объявлений с "ранним доступом".
    """
    logger.info(f"Delayed Worker запущен. Интервал проверки: {CHECK_INTERVAL} сек.")

    try:
        while True:
            # Получаем задачи, время раскрытия контактов которых уже наступило
            ready_tasks = await queue_manager.get_ready_delayed_task()

            if ready_tasks:
                logger.info(f"Найдено готовых отложенных задач: {len(ready_tasks)}")

                for task in ready_tasks:
                    external_id = task.get("external_id", "Unknown")
                    logger.info(f"Возвращаем Лид ID {external_id} в Main Queue для финальной обработки...")

                    # TODO: В будущем здесь можно вызвать парсер для обновления номера телефона
                    # перед отправкой в основную очередь.

                    # Перекладываем в основную очередь
                    await queue_manager.push_to_main(task)

            # Спим до следующей проверки
            await asyncio.sleep(CHECK_INTERVAL)

    except asyncio.CancelledError:
        logger.info("Delayed Worker останавливается...")
    finally:
        await queue_manager.close()

if __name__ == "__main__":
    asyncio.run(run_delayed_worker())