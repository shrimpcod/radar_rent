from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Call(Base):
    __tablename__ = 'calls'
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Запись звонка (путь к файлу или URL)
    recording_url = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    call_datetime = Column(DateTime, nullable=False)
    
    lead_actions = relationship("LeadAction", back_populates="call")
