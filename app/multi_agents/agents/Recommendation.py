from crewai import Agent
from tools.jsontool import JSONDatabase
from langchain_openai import ChatOpenAI

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
            JSONDatabase()
        ],
        llm=ChatOpenAI(model="gpt-4", temperature=0.6)
    )