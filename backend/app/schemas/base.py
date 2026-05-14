from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Базовая схема для всех Pydantic моделей.
    
    Используется как общий предок для всех схем.
    Может содержать общие поля и методы.
    """
    
    class Config:
        from_attributes = True  # Позволяет создавать схемы из SQLAlchemy моделей
