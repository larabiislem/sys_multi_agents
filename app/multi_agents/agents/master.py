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
        llm=get_llm(),
        memory=True
    )