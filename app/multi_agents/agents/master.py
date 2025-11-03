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




def create_master_orchestrator() -> Agent:
    return Agent(
        role='Master Orchestrator',
        goal='Route student requests to the appropriate specialized agent and ensure seamless interactions',
        backstory="""You are the central intelligence of ClubEvent Hub, a sophisticated 
        AI system that understands student needs and directs them to the right specialist. 
        You have deep knowledge of all available agents and their capabilities. You maintain 
        conversation context and provide backup responses when needed.""",
        verbose=True,
        allow_delegation=True,
         tools=[
            DatabaseTool()
        ],
        llm= MODEL,
         memory=True
    )