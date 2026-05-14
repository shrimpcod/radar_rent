from datetime import datetime
from typing import Optional
from .base import BaseSchema


class LeadResponse(BaseSchema):
    """Схема для ответа API."""

    id: int
    external_id: str
    external_url: Optional[str] = None
    price: float
    rooms_count: int
    area: float
    floor: int
    floors_count: int
    city: str
    metro_station: Optional[str] = None
    address: str
    phone_number: Optional[str] = None
    is_early_access: bool
    phone_reveal_at: Optional[datetime] = None
    published_offer_at: Optional[datetime] = None
    created_offer_at: Optional[datetime] = None
    source: Optional[str] = None
    photo_urls: Optional[list[str]] = None

