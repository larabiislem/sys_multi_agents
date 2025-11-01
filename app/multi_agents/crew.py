from crewai import Crew, Process
from .agents.master import create_master_orchestrator
from .agents.club_chatboot import create_club_chatbot
from .agents.Recommendation import create_recommendation_agent
from .agents.search_agent import create_search_agent
from .agents.onboarding_agent import create_onboarding_agent
from .tasks.master_task import create_routing_task
from .tasks.recemndation import create_weekly_digest_task
from .tasks.clubchatboot import create_club_info_task
from .tasks.onboarding import create_onboarding_task
from .tasks.recemndation import create_personalized_recommendations_task
from .tasks.search_tasks import create_search_task
from typing import Dict, Any

class ClubEventHubCrew:
    
    
    def __init__(self):
        self.master_orchestrator = create_master_orchestrator()
        self.recommendation_agent = create_recommendation_agent()
        self.search_agent = create_search_agent()
        self.onboarding_agent = create_onboarding_agent()
        self.club_chatbots = {} 
    
    def get_club_chatbot(self, club_id: str, personality: str = "friendly"):
        
        if club_id not in self.club_chatbots:
            self.club_chatbots[club_id] = create_club_chatbot(club_id, personality)
        return self.club_chatbots[club_id]
    
    def process_student_query(self, student_query: str, context: Dict[str, Any] = None) -> str:
  
        if context is None:
            context = {}
     
        routing_task = create_routing_task(self.master_orchestrator, student_query)
        
    
        routing_crew = Crew(
            agents=[self.master_orchestrator],
            tasks=[routing_task],
            process=Process.sequential,
            verbose=True
        )
  
        routing_result = routing_crew.kickoff()
        
        return routing_result
    
    def handle_club_query(self, club_id: str, student_question: str, club_personality: str = "friendly"):
   
   
    
        
        club_agent = self.get_club_chatbot(club_id, club_personality)
        task = create_club_info_task(club_agent, club_id, student_question)
        
        crew = Crew(
            agents=[club_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def handle_recommendation_request(self, student_id: str):

        
        
        task = create_personalized_recommendations_task(self.recommendation_agent, student_id)
        
        crew = Crew(
            agents=[self.recommendation_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def handle_search_query(self, search_query: str, filters: dict = None):
        
       
        
        task = create_search_task(self.search_agent, search_query, filters)
        
        crew = Crew(
            agents=[self.search_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def handle_onboarding(self, student_id: str):


        
        task = create_onboarding_task(self.onboarding_agent, student_id)
        
        crew = Crew(
            agents=[self.onboarding_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def handle_weekly_digest(self, student_id: str):

        
        
        task = create_weekly_digest_task(self.recommendation_agent, student_id)
        
        crew = Crew(
            agents=[self.recommendation_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()