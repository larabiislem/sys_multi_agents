from crewai import Task
from typing import List

def create_routing_task(agent, student_query: str) -> Task:
    """Create a task for routing student requests"""
    return Task(
        description=f"""You are an intelligent and friendly campus assistant who answers student questions in a natural, conversational way — like a human chat partner.

When the student asks a question, use the most relevant information from the available agents to provide a smooth, paragraph-style answer. 
Do not use bullet points or structured lists unless the student specifically asks for them. 
Make your response feel engaging, warm, and human — while staying accurate and informative.

Student Question: {student_query}

Available agents and their knowledge:
1. Club Chatbot - Information about clubs (activities, members, events, how to join, etc.)
2. Recommendation Agent - Personalized suggestions for clubs or activities
3. Search Agent - Details about upcoming events or opportunities
4. Onboarding Agent - Assistance with new users or profile setup

Respond only based on the student’s question and relevant data from the appropriate agent.
Do not mention or describe the agents. 
Write the answer as a natural paragraph that would feel like chatting with a helpful friend.

""",
        agent=agent,
        expected_output="Agent routing decision with context for the next agent"
    )

def create_context_management_task(agent, conversation_history: List[dict]) -> Task:
    
    return Task(
        description=f"""Maintain and update the conversation context based on the 
        conversation history:
        
        {conversation_history}
        
        Ensure continuity and provide backup responses if needed.""",
        agent=agent,
        expected_output="Updated conversation context and any necessary backup responses"
    )