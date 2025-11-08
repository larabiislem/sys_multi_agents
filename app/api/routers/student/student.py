from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_session
from models import Student, StudentProfile
from api.schemas.student import *
from ..autontification.haching import Hash
from ..autontification.token import get_current_user, TokenData

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)





def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()




@router.get("/", response_model=StudentResponse, status_code=status.HTTP_200_OK)
async def get_student(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.email == current_user.email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/", response_model=StudentResponse, status_code=status.HTTP_200_OK)
async def update_student(
    student_update: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.email == current_user.email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student_update.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["password_hash"] = Hash.hash_password(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(student, field, value)

    student.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(student)
    return student


@router.delete("/", response_model=DeleteResponse, status_code=status.HTTP_200_OK)
async def delete_student(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.email == current_user.email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return DeleteResponse(
        success=True,
        message="Student deleted successfully",
        timestamp=datetime.utcnow()
    )



@router.post("/profile", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.email == current_user.email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    existing_profile = db.query(StudentProfile).filter(
        StudentProfile.student_id == student.id
    ).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")

    new_profile = StudentProfile(
        student_id=student.id,
        bio=profile.bio,
        goals=profile.goals,
        notification_preferences=profile.notification_preferences
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile


@router.get("/profile", response_model=ProfileResponse, status_code=status.HTTP_200_OK)
async def get_profile(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.email == current_user.email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    profile = db.query(StudentProfile).filter(
        StudentProfile.student_id == student.id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.put("/profile", response_model=ProfileResponse, status_code=status.HTTP_200_OK)
async def update_profile(
    profile_update: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.email == current_user.email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    profile = db.query(StudentProfile).filter(
        StudentProfile.student_id == student.id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    profile.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(profile)
    return profile


@router.delete("/profile", response_model=DeleteResponse, status_code=status.HTTP_200_OK)
async def delete_profile(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.email == current_user.email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    profile = db.query(StudentProfile).filter(
        StudentProfile.student_id == student.id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    db.delete(profile)
    db.commit()

    return DeleteResponse(
        success=True,
        message="Profile deleted successfully",
        timestamp=datetime.utcnow()
    )
