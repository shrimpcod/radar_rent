from datetime import date
from .base import BaseSchema

class FavoriteBase(BaseSchema):
    lead_id: int
    user_id: int

class FavoriteCreate(FavoriteBase):
    pass 

class FavoriteResponse(FavoriteBase):
    id: int
    created_at: date

    class Config:
        from_attributes = True