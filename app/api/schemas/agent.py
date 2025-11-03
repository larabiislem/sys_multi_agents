
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class ChatRequest(BaseModel):
    club_id: int = Field(..., description="Club ID")
    question: str = Field(..., description="Student's question")
    club_personality: Optional[str] = Field(None, description="Club personality style")
    
    class Config:
        json_schema_extra = {
            "example": {
                "club_id": 1,
                "question": "What events do you have this month?",
                "club_personality": "friendly"
            }
        }


class ChatResponse(BaseModel):
    response: str = Field(..., description="Agent's response")
    club_name: str = Field(..., description="Club name")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Here are our upcoming events...",
                "club_name": "AI & Machine Learning Club"
            }
        }


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Agent processing failed",
                "detail": "Unable to connect to database"
            }
        }


class AgentRequest(BaseModel):
    message: str = Field(..., description="User's message or query")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional context")


class AgentResponse(BaseModel):
    response: str = Field(..., description="Agent's response")
    agent: str = Field(..., description="Which agent responded")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatbotRequest(BaseModel):
    club_id: int = Field(..., description="Club ID")
    message: str = Field(..., description="User's message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "club_id": 1,
                "message": "What is this club about?"
            }
        }


class RecommendationRequest(BaseModel):
    student_id: int = Field(..., description="Student ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "student_id": 1
            }
        }


class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "AI workshop",
                "filters": {"event_type": "workshop"}
            }
        }


class QueryRequest(BaseModel):
    query: str = Field(..., description="General query")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional context")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Show me AI events",
                "context": {}
            }
        }


class QueryResponse(BaseModel):
    response: str = Field(..., description="Response to the query")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Here are the available AI events..."
            }
        }


class OnboardingRequest(BaseModel):
    student_id: int = Field(..., description="Student ID for onboarding")
    
    class Config:
        json_schema_extra = {
            "example": {
                "student_id": 1
            }
        }


class OnboardingResponse(BaseModel):
    response: str = Field(..., description="Onboarding response")
    student_name: str = Field(..., description="Student name")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Welcome to ClubEvent Hub!",
                "student_name": "John Doe"
            }
        }


class RecommendationResponse(BaseModel):
    recommendations: str = Field(..., description="Recommendations for the student")
    student_name: str = Field(..., description="Student name")
    count: int = Field(..., description="Number of recommendations")
    
    class Config:
        json_schema_extra = {
            "example": {
                "recommendations": "Recommended events for you...",
                "student_name": "John Doe",
                "count": 5
            }
        }


class WeeklyDigestRequest(BaseModel):
    student_id: int = Field(..., description="Student ID for weekly digest")
    
    class Config:
        json_schema_extra = {
            "example": {
                "student_id": 1
            }
        }


class WeeklyDigestResponse(BaseModel):
    digest: str = Field(..., description="Weekly digest content")
    student_name: str = Field(..., description="Student name")
    
    class Config:
        json_schema_extra = {
            "example": {
                "digest": "Your weekly club and event digest...",
                "student_name": "John Doe"
            }
        }


class SearchResponse(BaseModel):
    results: str = Field(..., description="Search results")
    query: str = Field(..., description="Original search query")
    count: int = Field(..., description="Number of results")
    
    class Config:
        json_schema_extra = {
            "example": {
                "results": "Search results for AI events...",
                "query": "AI workshop",
                "count": 3
            }
        }