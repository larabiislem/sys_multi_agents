from crewai import Agent
from tools.jsontool import JSONDatabase
from langchain_openai import ChatOpenAI

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
            JSONDatabase()
        ],
        llm=ChatOpenAI(model="gpt-4", temperature=0.5)
    )