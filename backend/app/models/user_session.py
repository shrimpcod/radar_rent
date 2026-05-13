from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class UserSession(Base):
    __tablename__ = 'user_sessions'
         
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_date = Column(Date, nullable=False)
    login_at = Column(DateTime, nullable=False)
    logout_at = Column(DateTime, nullable=True)
    time_in_the_system = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="sessions")