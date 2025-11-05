from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_session
from models import Student, Club
from api.schemas.auth import *
from .haching import Hash
from .token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta, datetime

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

@router.post("/student/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse)
def register_student(student: StudentRegister, db: Session = Depends(get_db)):
    existing_student = db.query(Student).filter(Student.email == student.email).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = Hash.hash_password(student.password)
    
    new_student = Student(
        name=student.name,
        email=student.email,
        password_hash=hashed_password,
        field_of_study=student.field_of_study,
        year_level=student.year_level
    )
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return RegisterResponse(
        success=True,
        message="Student registered successfully",
        user_id=new_student.id,
        timestamp=datetime.utcnow()
    )

@router.post("/club/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse)
def register_club(club: ClubRegister, db: Session = Depends(get_db)):
    existing_club = db.query(Club).filter(Club.email == club.email).first()
    if existing_club:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = Hash.hash_password(club.password)
    
    new_club = Club(
        name=club.name,
        email=club.email,
        password_hash=hashed_password,
        description=club.description,
        mission=club.mission,
        contact_email=club.contact_email,
        website=club.website,
        personality_style=club.personality_style
    )
    
    db.add(new_club)
    db.commit()
    db.refresh(new_club)
    
    return RegisterResponse(
        success=True,
        message="Club registered successfully",
        user_id=new_club.id,
        timestamp=datetime.utcnow()
    )

@router.post("/student/login", status_code=status.HTTP_200_OK, response_model=Token)
def login_student(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.email == user.username).first()
    if not db_student or not Hash.verify_password(user.password, db_student.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_type": "student", "user_id": db_student.id}, 
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@router.post("/club/login", status_code=status.HTTP_200_OK, response_model=Token)
def login_club(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_club = db.query(Club).filter(Club.email == user.username).first()
    if not db_club or not Hash.verify_password(user.password, db_club.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_type": "club", "user_id": db_club.id}, 
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@router.get("/students", status_code=status.HTTP_200_OK)
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return [{"id": s.id, "name": s.name, "email": s.email, "field_of_study": s.field_of_study} for s in students]

@router.get("/clubs", status_code=status.HTTP_200_OK)
def get_clubs(db: Session = Depends(get_db)):
    clubs = db.query(Club).all()
    return [{"id": c.id, "name": c.name, "email": c.email, "description": c.description} for c in clubs]