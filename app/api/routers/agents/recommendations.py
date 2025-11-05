from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_session
from models import Student
from ...schemas.agent import (
    RecommendationRequest, RecommendationResponse,
    WeeklyDigestRequest, WeeklyDigestResponse,
    ErrorResponse
)
from multi_agents.crew import ClubEventHubCrew
from ..autontification.token import get_current_user 
import logging
import json

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)

logger = logging.getLogger(__name__)

crew_instance = None
def get_crew():
    global crew_instance
    if crew_instance is None:
        crew_instance = ClubEventHubCrew()
    return crew_instance


@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(
    db: Session = Depends(get_session),
   current_user=Depends(get_current_user)
):
  
    student_email = current_user.get("email")
    student = db.query(Student).filter(Student.email == student_email).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with email {student_email} not found"
        )

    crew = get_crew()
    logger.info(f"Generating recommendations for student {student.name} (ID: {student.id})")

    recommendations = crew.handle_recommendation_request(str(student.id))

    logger.info(f"Successfully generated recommendations for student {student.name}")

    try:
        rec_data = json.loads(str(recommendations))
        count = len(rec_data) if isinstance(rec_data, list) else 0
    except Exception:
        count = 0

    return RecommendationResponse(
        recommendations=str(recommendations),
        student_name=student.name,
        count=count
    )
