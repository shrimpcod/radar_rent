from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Messenger(Base):
    __tablename__ = "messengers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    user_messengers = relationship("UserMessenger", back_populates="messenger")
    