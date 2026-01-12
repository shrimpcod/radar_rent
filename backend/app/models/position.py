from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship 
from .base import Base 

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    
    users = relationship("User", back_populates="position")