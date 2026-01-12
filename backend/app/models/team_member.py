from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship 
from .base import Base

class TeamPosition(str, enum.Enum):
    HEAD = "head"
    MEMBER = "member" 

class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    team_position = Column(SQLEnum(TeamPosition), default=TeamPosition.MEMBER, nullable=False)

    team = relationship("Team", back_populates="team_members")
    user = relationship("User", back_populates="team_members")