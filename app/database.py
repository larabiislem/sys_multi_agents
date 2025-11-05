import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Try multiple paths for .env file
load_dotenv(dotenv_path="../.env.test")
load_dotenv(dotenv_path=".env")
load_dotenv()  # Look in current directory

Base = declarative_base()

def get_engine():
    DATABASE_URL = os.getenv('DATABASE_URL')

    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    # Removed print statement to avoid exposing secrets in logs
    return create_engine(DATABASE_URL, echo=True)



def init_db():

    from models.student import Student, StudentProfile
    from models.club import Club
    from models.event import Event
    from models.skils import Skill
    from models.relations import (
        student_skills, event_skills,
        event_registrations, club_members
    )
    
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("✅ Database tables created successfully!")


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def get_db():

    db = get_session()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    init_db()