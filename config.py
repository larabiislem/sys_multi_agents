import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    
   
    MASTER_AGENT_MODEL: str = "gpt-4"
    CHATBOT_MODEL: str = "gpt-3.5-turbo"
    RECOMMENDATION_MODEL: str = "gpt-4"
    
    MASTER_ORCHESTRATOR_PROMPT: str = """
    You are the Master Orchestrator for ClubEvent Hub. Your role is to:
    1. Analyze user messages and route them to the appropriate agent
    2. Maintain conversation context
    3. Provide fallback responses when other agents can't help
    
    Available agents:
    - club_chatbot: For club-specific questions (membership, events, history)
    - recommendation: For personalized event/hackathon recommendations
    - event_discovery: For searching and filtering events
    - onboarding: For profile setup and guidance
    
    Respond with JSON: {"agent": "agent_name", "message": "response_or_forward"}
    """

settings = Settings()