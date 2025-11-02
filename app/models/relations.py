from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from ..database import Base



student_skills = Table(
    'student_skills',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id', ondelete='CASCADE')),
    Column('skill_id', Integer, ForeignKey('skills.id', ondelete='CASCADE'))
)

event_skills = Table(
    'event_skills',
    Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id', ondelete='CASCADE')),
    Column('skill_id', Integer, ForeignKey('skills.id', ondelete='CASCADE'))
)

event_registrations = Table(
    'event_registrations',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id', ondelete='CASCADE')),
    Column('event_id', Integer, ForeignKey('events.id', ondelete='CASCADE')),
    Column('registered_at', DateTime, default=datetime.utcnow)
)

club_members = Table(
    'club_members',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id', ondelete='CASCADE')),
    Column('club_id', Integer, ForeignKey('clubs.id', ondelete='CASCADE')),
    Column('joined_at', DateTime, default=datetime.utcnow),
    Column('role', String(50), default='member')
)