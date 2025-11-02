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

def create_search_agent() -> Agent:
    """Create the Event Discovery and Search Agent"""
    return Agent(
        role='Event Discovery and Search Specialist',
        goal='Help students find specific events and opportunities quickly using natural language understanding',
        backstory="""You are a search expert who understands how students naturally express 
        their interests. You process natural language queries, understand synonyms and context 
        (like 'coding' means 'programming'), and provide relevant results. You can filter by 
        date, club, location, and skills. You highlight trending events and those with limited 
        seats to help students not miss out on great opportunities.""",
        verbose=True,
        allow_delegation=False,
          tools=[
            DatabaseTool()
        ],
        llm=get_llm(),
         memory=True
    )