import asyncio
import random 

async def random_delay(min_sec: float = 3.0, max_sec = 7.0):
    """Слуйчайная задержка между запросами для иммитации человека"""
    delay = random.uniform(min_sec, max_sec)
    await asyncio.sleep(delay)