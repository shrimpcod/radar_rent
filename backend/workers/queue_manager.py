import json 
import time
from typing import Optional, Dict, Any, List
from redis.asyncio import Redis

MAIN_QUEUE_NAME = "radar_main_queue"
DELAYED_QUEUE_NAME = "radar_delayed_queue"

class QueueManager:
    """
    Управление очередями задач на базе in-memory хранилища Redis.
    Реализует паттерн Producer-Consumer.
    """
    def __init__(self, redis_url: str):
        self.redis = Redis.from_url(redis_url, decode_responses=True)

    async def close(self):
        """Закрывает соединение с Redis"""
        await self.redis.close()

     # --- MAIN QUEUE (Основная очередь - Список FIFO) ---
    
    async def push_to_main(self, lead_data: Dict[str, Any]) -> None:
        """Помещает данные в конец основной очереди."""
        data_str = json.dumps(lead_data, ensure_ascii=False, default=str)
        await self.redis.rpush(MAIN_QUEUE_NAME, data_str)

    async def pop_from_main(self, timeout: int = 5) -> Optional[Dict[str, Any]]:
        """
        Блокирующее чтение из начала основной очереди.
        Если очередь пуста, воркер ждет timeout секунд, не расходуя CPU.
        """
        result = await self.redis.blpop(MAIN_QUEUE_NAME, timeout=timeout)
        if result:
            _, data_str = result
            return json.loads(data_str)
        return None
    
    # --- DELAYED QUEUE (Отложенная очередь - Сортированное множество ZSET) ---

    async def push_to_delayed(self, lead_data: Dict[str, Any], reveal_timestamp: int) -> None: 
        """
        Помещает лид с "ранним доступом" в отложенную очередь.
        reveal_timestamp (UNIX-время) используется как 'score' для сортировки.
        """

        data_str = json.dumps(lead_data, ensure_ascii=False, default=str)
        await self.redis.zadd(DELAYED_QUEUE_NAME, mapping={data_str: reveal_timestamp})

    async def get_ready_delayed_task(self) -> List[Dict[str, Any]]:
        """
        Извлекает задачи, время выполнения которых (score) <= текущему времени.
        """

        current_timestamp = int(time.time())
        
        ready_tasks_strs = await self.redis.zrangebyscore(
            DELAYED_QUEUE_NAME, min=0, max=current_timestamp
        )
    
        ready_tasks = []
        if ready_tasks_strs:
            await self.redis.zrem(DELAYED_QUEUE_NAME, *ready_tasks_strs)
            for task_str in ready_tasks_strs:
                ready_tasks.append(json.loads(task_str))

        return ready_tasks
    
from app.core.config import settings
queue_manager = QueueManager(redis_url=settings.REDIS_URL)
