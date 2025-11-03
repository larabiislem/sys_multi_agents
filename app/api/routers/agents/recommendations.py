from fastapi import APIRouter, HTTPException, status, Depends
from ...schemas.agent import (
    RecommendationRequest, RecommendationResponse,
    WeeklyDigestRequest, WeeklyDigestResponse,
    ErrorResponse
)
from multi_agents.crew import ClubEventHubCrew
from models import Student
from database import get_session
from sqlalchemy.orm import Session
import logging

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])
logger = logging.getLogger(__name__)


crew_instance = None

def get_crew():
    global crew_instance
    if crew_instance is None:
        crew_instance = ClubEventHubCrew()
    return crew_instance


@router.post("/",response_model=RecommendationResponse, )
async def get_recommendations(request: RecommendationRequest,db: Session = Depends(get_session)):

        student = db.query(Student).filter(Student.id == request.student_id).first()
        db.close()
        
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {request.student_id} not found"
            )


        crew = get_crew()
        logger.info(f"Generating recommendations for student {student.name} (ID: {request.student_id})")
        
        recommendations = crew.handle_recommendation_request(str(request.student_id))
        
        logger.info(f"Successfully generated recommendations for student {student.name}")
        
        import json
        try:
            rec_data = json.loads(str(recommendations))
            count = len(rec_data) if isinstance(rec_data, list) else 0
        except:
            count = 0
        
        return RecommendationResponse(
            recommendations=str(recommendations),
            student_name=student.name,
            count=count
        )
        



