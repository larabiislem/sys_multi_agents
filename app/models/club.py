from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from .relations import club_members


class Club(Base):
    __tablename__ = 'clubs'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    mission = Column(Text)
    history = Column(Text)
    contact_email = Column(String(100))
    website = Column(String(200))
    logo_url = Column(String(200))
    personality_style = Column(String(50))  # e.g., 'formal', 'casual', 'tech-focused'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    events = relationship('Event', back_populates='club', cascade='all, delete-orphan')
    members = relationship('Student', secondary=club_members, back_populates='clubs')

    def __repr__(self):
        return f"<Club(id={self.id}, name='{self.name}')>"
    
    @property
    def member_count(self):
        """Get the number of members in the club"""
        return len(self.members)