from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship 
from .base import Base 

class Agency(Base):
    __tablename__ = 'agencies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    users = relationship("User", back_populates="agency")
    teams = relationship("Team", back_populates="agency")