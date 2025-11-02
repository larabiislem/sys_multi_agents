from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from models.relations  import student_skills, event_registrations, club_members


class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    field_of_study = Column(String(100))
    year_level = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    skills = relationship('Skill', secondary=student_skills, back_populates='students')
    registered_events = relationship('Event', secondary=event_registrations, back_populates='registered_students')
    clubs = relationship('Club', secondary=club_members, back_populates='members')
    profile = relationship('StudentProfile', back_populates='student', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', email='{self.email}')>"


class StudentProfile(Base):
    __tablename__ = 'student_profiles'
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), unique=True, nullable=False)
    bio = Column(Text)
    goals = Column(Text)
    notification_preferences = Column(Text)  # JSON string
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    student = relationship('Student', back_populates='profile')

    def __repr__(self):
        return f"<StudentProfile(id={self.id}, student_id={self.student_id})>"