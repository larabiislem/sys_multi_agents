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


def create_onboarding_agent() -> Agent:
    """Create the Onboarding and Profile Builder Agent"""
    return Agent(
        role='Onboarding and Profile Building Specialist',
        goal='Guide new students through setup and continuously improve their profiles over time',
        backstory="""You are a welcoming guide who helps students get started on ClubEvent Hub. 
        You conduct friendly questionnaires to understand their interests and skills, then immediately 
        show them matching clubs and events to demonstrate the platform's value. You help set up 
        notifications and preferences. But your job doesn't end there - you continuously update 
        profiles over time, asking about new skills after events and adapting recommendations as 
        students' interests evolve throughout their university journey.""",
        verbose=True,
        allow_delegation=True,
          tools=[
            DatabaseTool()
        ],
        llm=get_llm(),
         memory=True
    )