from crewai.tools import BaseTool
from typing import Type, Dict, Any
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from models import (
    get_session, Student, StudentProfile, Club, Event, Skill
)
from datetime import datetime, timedelta
import json


class DatabaseToolInput(BaseModel):
    """Input schema for DatabaseTool."""
    operation: str = Field(..., description="The database operation to perform")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parameters for the operation")


class DatabaseTool(BaseTool):
    name: str = "Database Query Tool"
    description: str = """
    A comprehensive tool for querying and updating the ClubEvent Hub database.
    
    Available operations:
    - get_student: Get student information by ID or email
    - get_club: Get club information by ID or name
    - get_events: Get events with optional filters
    - search_events: Search events by query and filters
    - get_recommendations: Get personalized recommendations for a student
    - update_profile: Update student profile information
    - register_event: Register a student for an event
    - get_trending_events: Get currently trending events
    - get_club_members: Get members of a specific club
    - get_similar_students: Find students with similar skills
    """
    args_schema: Type[BaseModel] = DatabaseToolInput

    def _run(self, operation: str, parameters: Dict[str, Any]) -> str:
        """Execute database operations"""
        session = get_session()
        try:
            if operation == "get_student":
                return self._get_student(session, parameters)
            elif operation == "get_club":
                return self._get_club(session, parameters)
            elif operation == "get_events":
                return self._get_events(session, parameters)
            elif operation == "search_events":
                return self._search_events(session, parameters)
            elif operation == "get_recommendations":
                return self._get_recommendations(session, parameters)
            elif operation == "update_profile":
                return self._update_profile(session, parameters)
            elif operation == "register_event":
                return self._register_event(session, parameters)
            elif operation == "get_trending_events":
                return self._get_trending_events(session, parameters)
            elif operation == "get_club_members":
                return self._get_club_members(session, parameters)
            elif operation == "get_similar_students":
                return self._get_similar_students(session, parameters)
            elif operation == "get_all_students":
                return self._get_all_students(session, parameters)
            elif operation == "get_all_clubs":
                return self._get_all_clubs(session, parameters)
            elif operation == "get_all_skills":
                return self._get_all_skills(session, parameters)
            else:
                return json.dumps({"error": f"Unknown operation: {operation}"})
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            session.close()

    def _get_student(self, session: Session, params: Dict) -> str:
        """Get student information"""
        student_id = params.get('student_id')
        email = params.get('email')
        
        if student_id:
            student = session.query(Student).filter(Student.id == student_id).first()
        elif email:
            student = session.query(Student).filter(Student.email == email).first()
        else:
            return json.dumps({"error": "Either student_id or email is required"})
        
        if not student:
            return json.dumps({"error": "Student not found"})
        
        return json.dumps({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "field_of_study": student.field_of_study,
            "year_level": student.year_level,
            "skills": [{"id": skill.id, "name": skill.name, "category": skill.category} for skill in student.skills],
            "clubs": [{"id": club.id, "name": club.name} for club in student.clubs],
            "registered_events_count": len(student.registered_events),
            "profile": {
                "bio": student.profile.bio if student.profile else None,
                "goals": student.profile.goals if student.profile else None,
                "notification_preferences": student.profile.notification_preferences if student.profile else None
            }
        })

    def _get_club(self, session: Session, params: Dict) -> str:
        """Get club information"""
        club_id = params.get('club_id')
        club_name = params.get('club_name')
        
        if club_id:
            club = session.query(Club).filter(Club.id == club_id).first()
        elif club_name:
            club = session.query(Club).filter(Club.name.ilike(f"%{club_name}%")).first()
        else:
            return json.dumps({"error": "Either club_id or club_name is required"})
        
        if not club:
            return json.dumps({"error": "Club not found"})
        
        return json.dumps({
            "id": club.id,
            "name": club.name,
            "description": club.description,
            "mission": club.mission,
            "history": club.history,
            "contact_email": club.contact_email,
            "website": club.website,
            "personality_style": club.personality_style,
            "member_count": len(club.members),
            "upcoming_events": [
                {
                    "id": event.id,
                    "title": event.title,
                    "date": event.date.isoformat(),
                    "location": event.location,
                    "event_type": event.event_type
                }
                for event in club.events if event.date > datetime.utcnow()
            ][:10]
        })

    def _get_events(self, session: Session, params: Dict) -> str:
        """Get events with filters"""
        query = session.query(Event)
        
        if params.get('club_id'):
            query = query.filter(Event.club_id == params['club_id'])
        
        if params.get('date_from'):
            date_from = datetime.fromisoformat(params['date_from'])
            query = query.filter(Event.date >= date_from)
        
        if params.get('date_to'):
            date_to = datetime.fromisoformat(params['date_to'])
            query = query.filter(Event.date <= date_to)
        
        if params.get('event_type'):
            query = query.filter(Event.event_type == params['event_type'])
        
        # Only show future events by default
        if params.get('include_past') != True:
            query = query.filter(Event.date > datetime.utcnow())
        
        limit = params.get('limit', 20)
        events = query.order_by(Event.date).limit(limit).all()
        
        return json.dumps([
            {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "club_name": event.club.name,
                "club_id": event.club.id,
                "event_type": event.event_type,
                "location": event.location,
                "date": event.date.isoformat(),
                "deadline": event.deadline.isoformat() if event.deadline else None,
                "seats_available": event.seats_available,
                "is_full": event.is_full,
                "is_trending": event.is_trending,
                "required_skills": [skill.name for skill in event.required_skills]
            }
            for event in events
        ])

    def _search_events(self, session: Session, params: Dict) -> str:
        """Search events by query"""
        query_text = params.get('query', '')
        filters = params.get('filters', {})
        
        query = session.query(Event)
        
        # Text search
        if query_text:
            search_terms = query_text.lower().split()
            conditions = []
            for term in search_terms:
                conditions.append(
                    or_(
                        Event.title.ilike(f"%{term}%"),
                        Event.description.ilike(f"%{term}%"),
                        Event.event_type.ilike(f"%{term}%")
                    )
                )
            if conditions:
                query = query.filter(or_(*conditions))
        
        # Apply filters
        if filters.get('date_from'):
            query = query.filter(Event.date >= datetime.fromisoformat(filters['date_from']))
        if filters.get('date_to'):
            query = query.filter(Event.date <= datetime.fromisoformat(filters['date_to']))
        if filters.get('club_id'):
            query = query.filter(Event.club_id == filters['club_id'])
        if filters.get('event_type'):
            query = query.filter(Event.event_type == filters['event_type'])
        
        # Only future events
        query = query.filter(Event.date > datetime.utcnow())
        
        events = query.order_by(desc(Event.is_trending), Event.date).limit(20).all()
        
        return json.dumps([
            {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "club_name": event.club.name,
                "event_type": event.event_type,
                "location": event.location,
                "date": event.date.isoformat(),
                "is_trending": event.is_trending,
                "seats_available": event.seats_available
            }
            for event in events
        ])

    def _get_trending_events(self, session: Session, params: Dict) -> str:
        """Get trending events"""
        trending_events = session.query(Event).filter(
            and_(
                Event.date > datetime.utcnow(),
                Event.is_trending == True
            )
        ).order_by(desc(Event.view_count), desc(Event.current_registrations)).limit(10).all()
        
        return json.dumps([
            {
                "id": event.id,
                "title": event.title,
                "club_name": event.club.name,
                "date": event.date.isoformat(),
                "seats_remaining": event.seats_available,
                "registration_count": event.current_registrations,
                "view_count": event.view_count,
                "is_full": event.is_full
            }
            for event in trending_events
        ])

    def _get_recommendations(self, session: Session, params: Dict) -> str:
        """Get personalized recommendations for a student"""
        student_id = params.get('student_id')
        if not student_id:
            return json.dumps({"error": "student_id is required"})
        
        student = session.query(Student).filter(Student.id == student_id).first()
        if not student:
            return json.dumps({"error": "Student not found"})
        
        student_skill_ids = [s.id for s in student.skills]
        
        # Find events matching student skills
        upcoming_events = session.query(Event).filter(
            Event.date > datetime.utcnow()
        ).all()
        
        recommendations = []
        for event in upcoming_events:
            # Skip if already registered
            if event in student.registered_events:
                continue
            
            score = 0
            reasons = []
            
            # Check skill match
            event_skill_ids = [s.id for s in event.required_skills]
            matching_skills = set(student_skill_ids) & set(event_skill_ids)
            if matching_skills:
                skill_names = [s.name for s in event.required_skills if s.id in matching_skills]
                score += len(matching_skills) * 25
                reasons.append(f"Matches your skills: {', '.join(skill_names)}")
            
            # Check if student is in same club
            if event.club in student.clubs:
                score += 30
                reasons.append("Your club's event")
            
            # Trending bonus
            if event.is_trending:
                score += 15
                reasons.append("Trending event")
            
            # Popularity score
            score += event.view_count * 0.05
            
            if score > 0 or len(reasons) > 0:
                recommendations.append({
                    "item_id": event.id,
                    "item_type": "event",
                    "title": event.title,
                    "club_name": event.club.name,
                    "date": event.date.isoformat(),
                    "location": event.location,
                    "score": round(score, 2),
                    "reasons": reasons if reasons else ["Popular event"]
                })
        
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return json.dumps(recommendations[:15])

    def _update_profile(self, session: Session, params: Dict) -> str:
        """Update student profile"""
        student_id = params.get('student_id')
        if not student_id:
            return json.dumps({"error": "student_id is required"})
        
        student = session.query(Student).filter(Student.id == student_id).first()
        if not student:
            return json.dumps({"error": "Student not found"})
        
        # Update profile
        if not student.profile:
            student.profile = StudentProfile(student_id=student_id)
            session.add(student.profile)
        
        if 'bio' in params:
            student.profile.bio = params['bio']
        if 'goals' in params:
            student.profile.goals = params['goals']
        if 'notification_preferences' in params:
            student.profile.notification_preferences = json.dumps(params['notification_preferences'])
        
        # Update skills
        if 'skills' in params:
            skills = session.query(Skill).filter(
                Skill.name.in_(params['skills'])
            ).all()
            student.skills = skills
        
        # Update basic info
        if 'field_of_study' in params:
            student.field_of_study = params['field_of_study']
        if 'year_level' in params:
            student.year_level = params['year_level']
        
        session.commit()
        return json.dumps({"success": True, "message": "Profile updated successfully"})

    def _register_event(self, session: Session, params: Dict) -> str:
        """Register student for an event"""
        student_id = params.get('student_id')
        event_id = params.get('event_id')
        
        if not student_id or not event_id:
            return json.dumps({"error": "student_id and event_id are required"})
        
        student = session.query(Student).filter(Student.id == student_id).first()
        event = session.query(Event).filter(Event.id == event_id).first()
        
        if not student or not event:
            return json.dumps({"error": "Student or event not found"})
        
        # Check if already registered
        if event in student.registered_events:
            return json.dumps({"error": "Already registered for this event"})
        
        # Check if event is full
        if event.is_full:
            return json.dumps({"error": "Event is full"})
        
        # Check if event is in the past
        if event.is_past:
            return json.dumps({"error": "Cannot register for past events"})
        
        student.registered_events.append(event)
        event.current_registrations += 1
        
        session.commit()
        return json.dumps({
            "success": True,
            "message": f"Successfully registered for {event.title}",
            "event": {
                "id": event.id,
                "title": event.title,
                "date": event.date.isoformat()
            }
        })

    def _get_club_members(self, session: Session, params: Dict) -> str:
        """Get members of a club"""
        club_id = params.get('club_id')
        if not club_id:
            return json.dumps({"error": "club_id is required"})
        
        club = session.query(Club).filter(Club.id == club_id).first()
        if not club:
            return json.dumps({"error": "Club not found"})
        
        return json.dumps({
            "club_name": club.name,
            "member_count": len(club.members),
            "members": [
                {
                    "id": member.id,
                    "name": member.name,
                    "email": member.email,
                    "field_of_study": member.field_of_study,
                    "year_level": member.year_level
                }
                for member in club.members
            ]
        })

    def _get_similar_students(self, session: Session, params: Dict) -> str:
        """Find students with similar skills"""
        student_id = params.get('student_id')
        if not student_id:
            return json.dumps({"error": "student_id is required"})
        
        student = session.query(Student).filter(Student.id == student_id).first()
        if not student:
            return json.dumps({"error": "Student not found"})
        
        student_skill_ids = {s.id for s in student.skills}
        
        similar_students = []
        for other in session.query(Student).filter(Student.id != student_id).all():
            other_skill_ids = {s.id for s in other.skills}
            
            similarity = len(student_skill_ids & other_skill_ids)
            
            if similarity > 0:
                similar_students.append({
                    "id": other.id,
                    "name": other.name,
                    "field_of_study": other.field_of_study,
                    "similarity_score": similarity,
                    "common_skills": [s.name for s in other.skills if s.id in student_skill_ids]
                })
        
        similar_students.sort(key=lambda x: x['similarity_score'], reverse=True)
        return json.dumps(similar_students[:10])

    def _get_all_students(self, session: Session, params: Dict) -> str:
        """Get all students"""
        students = session.query(Student).all()
        return json.dumps([
            {
                "id": s.id,
                "name": s.name,
                "email": s.email,
                "field_of_study": s.field_of_study,
                "year_level": s.year_level
            }
            for s in students
        ])

    def _get_all_clubs(self, session: Session, params: Dict) -> str:
        """Get all clubs"""
        clubs = session.query(Club).all()
        return json.dumps([
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "member_count": len(c.members)
            }
            for c in clubs
        ])

    def _get_all_skills(self, session: Session, params: Dict) -> str:
        """Get all skills"""
        skills = session.query(Skill).all()
        return json.dumps([
            {
                "id": s.id,
                "name": s.name,
                "category": s.category
            }
            for s in skills
        ])