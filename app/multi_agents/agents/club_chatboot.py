from crewai import Agent
from ..tools.databasetool import DatabaseTool
import os
from dotenv import load_dotenv
from .openrouter import OpenRouterLLM


load_dotenv()





load_dotenv()

MODEL = OpenRouterLLM(
    model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
    api_key=os.getenv("OPENAI_API_KEY"),  # CrewAI lit ici
    base_url=os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")
)


def create_club_chatbot(club_id: str, club_personality: str = "friendly") -> Agent:
  
    return Agent(
        role=f'Club Chatbot for Club {club_id}',
        goal=f'Answer all questions about this club with a {club_personality} personality',
        backstory=f"""You are the dedicated AI assistant for this club. You know 
        everything about the club's history, members, events, requirements, and how to join. 
        You embody the club's {club_personality} personality in every interaction. You remember 
        past conversations with students and provide personalized, helpful responses. You help 
        with applications, share links, and explain requirements clearly.""",
        verbose=True,
        allow_delegation=False,
        llm=MODEL ,
        memory=True
    )