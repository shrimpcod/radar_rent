from sqlalchemy import Boolean, Column, Integer, String, Numeric, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from .base import Base

class Lead(Base):
    __tablename__ = 'leads'
    
    # Айдишки
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, nullable=False)
    external_url = Column(Text, nullable=True)  # URL на внешнем сайте (например, Циан)

    #Основные поля
    price = Column(Numeric, nullable=False)  # Цена
    area = Column(Numeric, nullable=False)  # Площадь (в кв.м)
    rooms_count = Column(Integer, nullable=False)  # Количество комнат
    floor = Column(Integer, nullable=False)  # Этаж
    floors_count = Column(Integer, nullable=False)  # Этажей в доме
    
    # Локация
    city = Column(String, nullable=False)  # Город
    metro_station = Column(String, nullable=True)  # Станция метро (опционально)
    address = Column(String, nullable=False)  # Полный адрес

    phone_number = Column(String, nullable=False)  # Номер телефона
    
    # Временные метки
    created_offer_at = Column(DateTime, nullable=False)  # Дата и время создания/публикации
    published_offer_at = Column(DateTime, nullable=True)  # Дата и время публикации на внешнем сайте
    
    #Ранний доступ
    is_early_access = Column(Boolean, nullable=False) 
    phone_reveal_at = Column(DateTime, nullable=True)


    source = Column(String, nullable=True)  # Источник (cian, avito и т.д.)
    photo_urls = Column(JSON, nullable=True)  # Массив URL фотографий
    
    # Связи
    lead_actions = relationship("LeadAction", back_populates="lead")

    #TODO: добавить поле источник