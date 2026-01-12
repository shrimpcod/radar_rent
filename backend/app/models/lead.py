from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base

class Lead(Base):
    __tablename__ = 'leads'
    
    # Основные поля
    id = Column(Integer, primary_key=True, index=True)
    
    # Информация об объекте недвижимости
    rooms_count = Column(Integer, nullable=False)  # Количество комнат
    city = Column(String, nullable=False)  # Город
    metro_station = Column(String, nullable=True)  # Станция метро (опционально)
    area = Column(Float, nullable=False)  # Площадь (в кв.м)
    floor = Column(Integer, nullable=False)  # Этаж
    price = Column(Float, nullable=False)  # Цена
    address = Column(String, nullable=False)  # Полный адрес
    phone_number = Column(String, nullable=False)  # Номер телефона
    
    # Связь с собственником
    owner_id = Column(Integer, ForeignKey('owners.id'), nullable=True)
    
    # Дополнительная информация
    created_at = Column(DateTime, nullable=False)  # Дата и время создания/публикации
    notes = Column(Text, nullable=True)  # Заметки (опционально)
    
    # Связи
    owner = relationship("Owner", back_populates="leads")
    lead_actions = relationship("LeadAction", back_populates="lead")
