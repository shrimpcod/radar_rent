import os 
import logging
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession 
from aiogram.types import LinkPreviewOptions
from app.core.config import settings
from .formatter import format_lead_card
from ..base.base_notifier import BaseNotifier

logger = logging.getLogger(__name__)

class TelegramNotifier(BaseNotifier):

    def __init__(self):
        proxy = settings.TELEGRAM_PROXY
        session = AiohttpSession(proxy=proxy, timeout=10) if proxy else None
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, session=session)

    async def send(self, lead) -> None:
        try:
            await self.bot.send_message(
                chat_id=settings.TELEGRAM_CHAT_ID,
                text=format_lead_card(lead),
                parse_mode="HTML",
                link_preview_options=LinkPreviewOptions(prefer_small_media=True, show_above_text=False)
            )
            logger.info(f"Отправлено в Telegram: {lead.external_id}")

        except Exception as e:
            logger.error(f"Ошибка отправки в Telegram: {e}")
        finally:
            await self.bot.session.close()