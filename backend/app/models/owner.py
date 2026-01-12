from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)

    leads = relationship("Lead", back_populates="owner")
    owner_contacts = relationship("OwnerContact", back_populates="owner")