from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from models.relations import event_skills, event_registrations


class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey('clubs.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    event_type = Column(String(50), index=True)  # e.g., 'workshop', 'hackathon', 'social', 'competition'
    location = Column(String(200))
    date = Column(DateTime, nullable=False, index=True)
    deadline = Column(DateTime)
    max_seats = Column(Integer)
    current_registrations = Column(Integer, default=0)
    is_trending = Column(Boolean, default=False, index=True)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    club = relationship('Club', back_populates='events')
    required_skills = relationship('Skill', secondary=event_skills, back_populates='events')
    registered_students = relationship('Student', secondary=event_registrations, back_populates='registered_events')

    def __repr__(self):
        return f"<Event(id={self.id}, title='{self.title}', date={self.date})>"
    
    @property
    def seats_available(self):
        """Get the number of available seats"""
        if self.max_seats is None:
            return None
        return max(0, self.max_seats - self.current_registrations)
    
    @property
    def is_full(self):
        """Check if the event is full"""
        if self.max_seats is None:
            return False
        return self.current_registrations >= self.max_seats
    
    @property
    def is_past(self):
        """Check if the event date has passed"""
        return self.date < datetime.utcnow()