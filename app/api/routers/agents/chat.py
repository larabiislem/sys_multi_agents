
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from ...schemas.agent import (
    ChatRequest, ChatResponse, ErrorResponse
)
from multi_agents.crew import ClubEventHubCrew
from models import Club
from database import get_session
import logging

router = APIRouter(prefix="/chat", tags=["Chat"])
logger = logging.getLogger(__name__)


crew_instance = None

def get_crew():
    global crew_instance
    if crew_instance is None:
        crew_instance = ClubEventHubCrew()
    return crew_instance


@router.post("/club",response_model=ChatResponse)
async def chat_with_club(request: ChatRequest ,  db: Session = Depends(get_session)):
   
        club = db.query(Club).filter(Club.id == request.club_id).first()
        db.close()
        
        if not club:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Club with ID {request.club_id} not found"
            )

        crew = get_crew()
        logger.info(f"Processing chat request for club {club.name} (ID: {request.club_id})")
        
        response = crew.handle_club_query(
            club_id=str(request.club_id),
            student_question=request.question,
            club_personality=request.club_personality or club.personality_style or "friendly"
        )
        
        logger.info(f"Successfully generated response for club {club.name}")
        
        return ChatResponse(
            response=str(response),
            club_name=club.name
        )
        
 




