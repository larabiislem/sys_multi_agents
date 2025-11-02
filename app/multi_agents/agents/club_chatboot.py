from crewai import Agent
from ..tools.databasetool import DatabaseTool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Configure ChatOpenAI for OpenRouter
def get_llm():
    return ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1"),
        model=os.getenv("OPENAI_MODEL", "openai/gpt-4o-mini"),
        temperature=0.3
    )
from dotenv import load_dotenv
import openai

load_dotenv()

# 🔧 Configuration OpenRouter
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")

# CrewAI compatibilité
os.environ["OPENAI_API_KEY"] = openai.api_key
os.environ["OPENAI_API_BASE"] = openai.api_base

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


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
        llm=get_llm(),
        memory=True
    )