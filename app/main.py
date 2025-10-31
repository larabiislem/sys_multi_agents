import os
from dotenv import load_dotenv
from multi_agents.crew import ClubEventHubCrew

# Load environment variables
load_dotenv()

def main():
    """Main application entry point"""
    
    # Initialize the crew
    crew = ClubEventHubCrew()
    
    print("=" * 60)
    print("Welcome to ClubEvent Hub AI Assistant")
    print("=" * 60)
    
    # Example 1: General query routing
    print("\n--- Example 1: General Query ---")
    result = crew.process_student_query(
        "I'm interested in AI and machine learning. What clubs should I join?"
    )
    print(f"\nResult: {result}")
    
    # Example 2: Club-specific query
    print("\n--- Example 2: Club Query ---")
    result = crew.handle_club_query(
        club_id="club123",
        student_question="How can I join the AI Club? What are the requirements?",
        club_personality="technical and innovative"
    )
    print(f"\nResult: {result}")
    
    # Example 3: Personalized recommendations
    print("\n--- Example 3: Recommendations ---")
    result = crew.handle_recommendation_request(student_id="student123")
    print(f"\nResult: {result}")
    
    # Example 4: Event search
    print("\n--- Example 4: Event Search ---")
    result = crew.handle_search_query(
        search_query="Show me AI events this month",
        filters={"category": "Technology"}
    )
    print(f"\nResult: {result}")
    
    # Example 5: Student onboarding
    print("\n--- Example 5: Onboarding ---")
    result = crew.handle_onboarding(student_id="student456")
    print(f"\nResult: {result}")
    
    # Example 6: Weekly digest
    print("\n--- Example 6: Weekly Digest ---")
    result = crew.handle_weekly_digest(student_id="student123")
    print(f"\nResult: {result}")

if __name__ == "__main__":
    main()