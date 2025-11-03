from crewai import Task

def create_club_info_task(agent, club_id: str, student_question: str) -> Task:
  
    return Task(
        description=f"""Answer the following question about Club {club_id}:

Question: {student_question}

Respond concisely and directly based on the question. 
Only include detailed information (such as history, mission, members, events, joining requirements, or resources) **if the user specifically asks for it** or if it is clearly relevant to the question.

Always match the club's personality and tone in your response.
""",
        agent=agent,
        expected_output="Detailed, personalized answer about the club"
    )

def create_application_help_task(agent, club_id: str, student_id: str) -> Task:
   
    return Task(
        description=f"""Help student {student_id} with the application process for Club {club_id}.
        
        Provide:
        1. Step-by-step application instructions
        2. Required documents or information
        3. Deadlines and timelines
        4. Application form links
        5. Contact information for follow-up questions""",
        agent=agent,
        expected_output="Complete application guidance with all necessary details"
    )