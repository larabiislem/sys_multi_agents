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


def create_recommendation_agent() -> Agent:
    """Create the Smart Recommendation Agent"""
    return Agent(
        role='Smart Recommendation Specialist',
        goal='Provide personalized recommendations for events, clubs, and opportunities based on student profiles and behavior',
        backstory="""You are an expert in recommendation systems and student engagement. 
        You analyze student profiles, academic fields, skills, and platform activity to suggest 
        the most relevant opportunities. You use advanced algorithms to find patterns from similar 
        students and understand timing factors like exam periods. You explain why each recommendation 
        is relevant, helping students discover opportunities they'll truly enjoy.""",
        verbose=True,
        allow_delegation=False,
           tools=[
            DatabaseTool()
        ],
        llm= MODEL,
         memory=True
    )