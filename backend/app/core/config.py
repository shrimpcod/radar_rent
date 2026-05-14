from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Radar Rent"
    DESCRIPTION: str = "Radar Rent — сервис мониторинга объявлений аренды недвижимости"
    DATABASE_URL: str  # Будет загружен из .env
    SECRET_KEY: str   # Будет загружен из .env
    REDIS_URL: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: int = 0
    TELEGRAM_PROXY: str | None = None

    PROXIES: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()