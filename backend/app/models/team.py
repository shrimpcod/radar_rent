from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint 
from sqlalchemy.orm import relationship 
from .base import Base 

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    agency_id = Column(Integer, ForeignKey('agencies.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('agency_id', 'name', name='uq_team_agency_name')
    )

    agency = relationship("Agency", back_populates="teams")
    team_members = relationship("TeamMember", back_populates="team")