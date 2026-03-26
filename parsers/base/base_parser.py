from abc import ABC, abstractmethod

class BaseParser(ABC):
    """
      Базовый класс для всех парсеров.
      Каждый новый парсер (ЦИАН, Авито и др.) наследует этот класс
      и реализует два метода.
    """

    @abstractmethod
    async def fetch_listings(self) -> list[dict]:
        """Сделать запрос к источнику и вернуть сырые данные"""
    
    @abstractmethod
    async def parse_offer(self, offer: dict) -> dict:
        """Преобразовать одно объявление в словарь для БД"""