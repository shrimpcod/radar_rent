from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from .constants import CHAT_ID, BOT_TOKEN
from datetime import datetime
from .formatters import format_lead_card
import asyncio

bot = Bot(token=BOT_TOKEN)

async def send_lead_to_tg(lead):

    try:
        message = format_lead_card(lead)
        await bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    except Exception as e:
        print(f"[{datetime.now()}] Ошибка отправки в Telegram: {e}")

dp = Dispatcher()
@dp.message(Command("start"))
async def cmd_start(message):
    await message.answer(
        "🏠 Добро пожаловать в Radar Rent!"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())