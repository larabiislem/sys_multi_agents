
from fastapi import APIRouter
from ...schemas.agent import (
    SearchRequest, SearchResponse, ErrorResponse
)
from multi_agents.crew import ClubEventHubCrew
import logging
import json

router = APIRouter(prefix="/search", tags=["Search"])
logger = logging.getLogger(__name__)


crew_instance = None

def get_crew():
    global crew_instance
    if crew_instance is None:
        crew_instance = ClubEventHubCrew()
    return crew_instance


@router.post(
    "/",
    response_model=SearchResponse,

)
async def search_events(request: SearchRequest):
 
        crew = get_crew()
        logger.info(f"Processing search query: '{request.query}'")
        
        results = crew.handle_search_query(
            search_query=request.query,
            filters=request.filters
        )
        
        logger.info(f"Search completed for query: '{request.query}'")
        
        # Count results (simple heuristic)
        try:
            results_data = json.loads(str(results))
            count = len(results_data) if isinstance(results_data, list) else 0
        except:
            count = 0
        
        return SearchResponse(
            results=str(results),
            query=request.query,
            count=count
        )
        



