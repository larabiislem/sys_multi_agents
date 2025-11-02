from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from models.relations import student_skills, event_skills


class Skill(Base):
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50), index=True)  # e.g., 'technical', 'soft_skill', 'language'
    
    # Relationships
    students = relationship('Student', secondary=student_skills, back_populates='skills')
    events = relationship('Event', secondary=event_skills, back_populates='required_skills')

    def __repr__(self):
        return f"<Skill(id={self.id}, name='{self.name}', category='{self.category}')>"