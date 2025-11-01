from crewai import Agent
from tools.jsontool import JSONDatabase
from langchain_openai import ChatOpenAI

def create_club_chatbot(club_id: str, club_personality: str = "friendly") -> Agent:
  
    return Agent(
        role=f'Club Chatbot for Club {club_id}',
        goal=f'Answer all questions about this club with a {club_personality} personality',
        backstory=f"""You are the dedicated AI assistant for this club. You know 
        everything about the club's history, members, events, requirements, and how to join. 
        You embody the club's {club_personality} personality in every interaction. You remember 
        past conversations with students and provide personalized, helpful responses. You help 
        with applications, share links, and explain requirements clearly.""",
        verbose=True,
        allow_delegation=False,
        tools=[
            JSONDatabase()
        ],
        llm=ChatOpenAI(model="gpt-4", temperature=0.8),
        memory=True
    )