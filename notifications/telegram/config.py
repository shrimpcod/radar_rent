import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID: int = int(os.getenv("TELEGRAM_CHAT_ID", "0"))