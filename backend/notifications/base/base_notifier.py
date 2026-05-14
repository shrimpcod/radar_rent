from abc import ABC, abstractmethod

class BaseNotifier(ABC):
    """
      Базовый класс для всех уведомлений.
      Каждый новый канал (Telegram, VK, Max и др.) наследует этот класс.
    """

    @abstractmethod
    async def send(self, lead) -> None:
        """Отправить уведомление о новом объявлении"""