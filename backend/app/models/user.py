from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .base import Base 
import enum

class UserType(str, enum.Enum):
    PRIVATE = "private"
    CORPORATE = "corporate"
    AGENCY_OWNER = "agency_owner"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    login = Column(String, unique=True, index=True, nullable=False)
    fullname = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(SQLEnum(UserType), default=UserType.PRIVATE, nullable=False)
    ip_address = Column(String, nullable=False)

    agency_id = Column(Integer, ForeignKey("agencies.id"), nullable=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=True)

    agency = relationship("Agency", back_populates="users")
    position = relationship("Position", back_populates="users")
    team_members = relationship("TeamMember", back_populates="user")
    user_messengers = relationship("UserMessenger", back_populates="user")
    lead_actions = relationship("LeadAction", back_populates="user")
