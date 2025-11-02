from crewai import Agent
from ..tools.databasetool import DatabaseTool
from langchain_openai import ChatOpenAI
import os


from langchain_openai import ChatOpenAI

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
        llm=ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            api_key=os.getenv("OPENAI_API_KEY")
        ),
         memory=True
    )