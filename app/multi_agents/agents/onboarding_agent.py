from crewai import Agent
from tools.jsontool import JSONDatabase
from langchain_openai import ChatOpenAI

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
            JSONDatabase()

            
        ],
        llm=ChatOpenAI(model="gpt-4", temperature=0.7),
        memory=True
    )