from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_session
from models import Club
from api.schemas.club import *
from ..autontification.haching import Hash
from ..autontification.token import get_current_user, TokenData

router = APIRouter(
    prefix="/clubs",
    tags=["Clubs"]
)


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()




@router.get("/", response_model=ClubResponse, status_code=status.HTTP_200_OK)
async def get_club(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    club = db.query(Club).filter(Club.email == current_user.email).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    return club


@router.put("/", response_model=ClubResponse, status_code=status.HTTP_200_OK)
async def update_club(
    club_update: ClubUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    club = db.query(Club).filter(Club.email == current_user.email).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    update_data = club_update.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["password_hash"] = Hash.hash_password(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(club, field, value)

    club.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(club)
    return club


@router.delete("/", response_model=DeleteResponse, status_code=status.HTTP_200_OK)
async def delete_club(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    club = db.query(Club).filter(Club.email == current_user.email).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    db.delete(club)
    db.commit()

    return DeleteResponse(
        success=True,
        message="Club deleted successfully",
        timestamp=datetime.utcnow()
    )
