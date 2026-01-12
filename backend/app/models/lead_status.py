from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class LeadStatus(Base):
    __tablename__ = 'lead_statuses'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  
    color = Column(String, nullable=False)  
    
    lead_actions = relationship("LeadAction", back_populates="lead_status")
