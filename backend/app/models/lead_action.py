from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class LeadAction(Base):
    __tablename__ = 'lead_actions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    lead_id = Column(Integer, ForeignKey('leads.id'), nullable=False)
    lead_status_id = Column(Integer, ForeignKey('lead_statuses.id'), nullable=True)
    call_id = Column(Integer, ForeignKey('calls.id'), nullable=True)
    
    is_favorite = Column(Boolean, default=False, nullable=False)
    last_action_time = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="lead_actions")
    lead = relationship("Lead", back_populates="lead_actions")
    lead_status = relationship("LeadStatus", back_populates="lead_actions")
    call = relationship("Call", back_populates="lead_actions")
