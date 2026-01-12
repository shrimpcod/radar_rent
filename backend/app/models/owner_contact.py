from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base
import enum

class ContactType(str, enum.Enum):
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"

class OwnerContact(Base):
    __tablename__ = "owner_contacts"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)
    contact_type = Column(SQLEnum(ContactType), nullable=False)
    contact = Column(String, unique=True, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('owner_id', 'contact', name='uq_owner_contact'),
    )
    
    owner = relationship("Owner", back_populates="owner_contacts")