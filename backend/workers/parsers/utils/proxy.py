import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


def load_proxies_from_env() -> list[str]:
    """Читает список прокси из переменной PROXIES в .env"""
    raw = settings.PROXIES
    return [p.strip() for p in raw.split(",") if p.strip()]


class ProxyManager:
    def __init__(self, proxies: list[str]):
        """
          proxies — список строк вида 'http://user:pass@host:port'
          Берётся из .env файла
        """
        self._proxies = list(proxies)
        self._index = 0

    def get_proxy(self) -> str | None:
        """Возвращает следующий прокси по кругу"""
        if not self._proxies:
            return None
        if self._index >= len(self._proxies):
            self._index = 0

        proxy = self._proxies[self._index]
        self._index = (self._index + 1) % len(self._proxies)
        return proxy
    
    def remove_proxy(self, proxy: str):
        """Удаляет прокси из пула если он заблокирован"""
        if proxy in self._proxies:
            self._proxies.remove(proxy)
            self._index = 0
            logger.warning(f"Прокси удалён из пула: {proxy}. Осталось: {len(self._proxies)}")
        if not self._proxies:
            self._proxies = load_proxies_from_env()
            self._index = 0
            logger.info(f"Пул прокси восстановлен: {len(self._proxies)} прокси")