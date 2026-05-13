import logging
from .config import CIAN_API_URL, CIAN_SEARCH_URL, SEARCH_PAYLOAD
from .mapper import map_offer
from ..base.base_parser import BaseParser
from ..base.http_client import make_session, _proxy_manager
from ..utils.retry import retry

logger = logging.getLogger(__name__)

class CianParser(BaseParser):

    async def fetch_listings(self) -> list[dict]:    
        total_proxies = max(1, len(_proxy_manager._proxies))

        async def perform_request():
            proxy = _proxy_manager.get_proxy()
            
            try:
                session = await make_session(proxy=proxy)

                async with session:
                    logger.info(f"Используем прокси {proxy}")
                    logger.info("Получаем cookies с главной страницы...")
                    await session.get(CIAN_SEARCH_URL, timeout=15)

                    logger.info("Делаем API запрос...")
                    response = await session.post(CIAN_API_URL, json=SEARCH_PAYLOAD, timeout=15)

                    if not response.text:
                        raise Exception("Циан вернул пустой ответ")

                    data = response.json()
                    offers = data.get('data', {}).get('offersSerialized', [])
                    logger.info(f"Найдено объявлений: {len(offers)}")
                    return offers

            except Exception as e:
                if proxy:
                    _proxy_manager.remove_proxy(proxy)
                    logger.warning(f"Прокси удалён из пула: {proxy}")
                raise

        return await retry(perform_request, max_attempts=total_proxies, base_delay=1.0)
        
    def parse_offer(self, offer) -> dict:
        return map_offer(offer)
        
