
from fastapi import APIRouter, HTTPException, status, Depends
from ...schemas.agent import (
    QueryRequest, QueryResponse,
    OnboardingRequest, OnboardingResponse,
    ErrorResponse
)
from multi_agents.crew import ClubEventHubCrew
from models import Student
from database import get_session
import logging
from sqlalchemy.orm import Session

router = APIRouter(prefix="/agents", tags=["Agents"])
logger = logging.getLogger(__name__)


crew_instance = None

def get_crew():
    global crew_instance
    if crew_instance is None:
        crew_instance = ClubEventHubCrew()
    return crew_instance


@router.post("/query",response_model=QueryResponse )
async def process_query(request: QueryRequest):

   
        crew = get_crew()
        logger.info(f"Processing general query: '{request.query[:50]}...'")
        
        response = crew.process_student_query(
            student_query=request.query,
            context=request.context
        )
        
        logger.info(f"Query processed successfully")
        
        return QueryResponse(
            response=str(response)
        )
        



@router.post("/onboarding",response_model=OnboardingResponse)
async def onboard_student(request: OnboardingRequest , db: Session = Depends(get_session)):
    student = db.query(Student).filter(Student.id == request.student_id).first()
    db.close()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {request.student_id} not found"
        )

    crew = get_crew()
    logger.info(f"Onboarding student {student.name} (ID: {request.student_id})")

    response = crew.handle_onboarding(str(request.student_id))

    logger.info(f"Successfully onboarded student {student.name}")

    return OnboardingResponse(
        response=str(response),
        student_name=student.name
    )
        
  
