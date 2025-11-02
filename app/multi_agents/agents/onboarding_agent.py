from crewai import Agent
from ..tools.databasetool import DatabaseTool
from langchain_openai import ChatOpenAI
import os

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
        llm=ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            api_key=os.getenv("OPENAI_API_KEY")
        ),
         memory=True
    )