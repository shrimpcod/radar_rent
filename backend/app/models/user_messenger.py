from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base

class UserMessenger(Base):
    __tablename__ = "user_messengers"

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    messenger_id = Column(Integer, ForeignKey("messengers.id"), nullable=False)
    messenger_identifier = Column(String, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'messenger_id', name='uq_user_messenger'),
    )
    
    user = relationship("User", back_populates="user_messengers")
    messenger = relationship("Messenger", back_populates="user_messengers")