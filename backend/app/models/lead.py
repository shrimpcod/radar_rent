from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base

class Lead(Base):
    __tablename__ = 'leads'
    
    # Айдишки
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, nullable=False)
    external_url = Column(String, nullable=True)  # URL на внешнем сайте (например, Циан)

    #Основные поля
    price = Column(Float, nullable=False)  # Цена
    area = Column(Float, nullable=False)  # Площадь (в кв.м)
    rooms_count = Column(Integer, nullable=False)  # Количество комнат
    floor = Column(Integer, nullable=False)  # Этаж
    floors_count = Column(Integer, nullable=False)  # Этажей в доме
    
    # Локация
    city = Column(String, nullable=False)  # Город
    metro_station = Column(String, nullable=True)  # Станция метро (опционально)
    address = Column(String, nullable=False)  # Полный адрес
    
    # Связь с собственником
    owner_id = Column(Integer, ForeignKey('owners.id'), nullable=True)
    #owner_offer_id = Column(Integer, nullable=True)
    phone_number = Column(String, nullable=False)  # Номер телефона
    
    # Дополнительная информация
    created_offer_at = Column(DateTime, nullable=False)  # Дата и время создания/публикации
    published_offer_at = Column(DateTime, nullable=True)  # Дата и время публикации на внешнем сайте
    
    #Ранний доступ
    is_early_access = Column(Boolean, nullable=False) 
    phone_reveal_at = Column(DateTime, nullable=True)


    notes = Column(Text, nullable=True)  # Заметки (опционально)
    
    # Связи
    owner = relationship("Owner", back_populates="leads")
    lead_actions = relationship("LeadAction", back_populates="lead")

    #TODO: добавить поле источник