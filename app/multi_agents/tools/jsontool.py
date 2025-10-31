from crewai_tools import tool
from typing import List, Dict, Any, Optional
import json
import os
from datetime import datetime
from pathlib import Path

class JSONDatabase:
    """Singleton JSON Database Manager"""
    _instance = None
    _data = {}
    
    DATA_DIR = Path("data")
    
    FILES = {
        "students": "students.json",
        "clubs": "clubs.json",
        "events": "events.json",
        "student_clubs": "student_clubs.json",
        "student_events": "student_events.json",
        "event_views": "event_views.json",
        "recommendations_history": "recommendations_history.json",
        "conversations": "conversations.json"
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JSONDatabase, cls).__new__(cls)
            cls._instance._load_all_data()
        return cls._instance
    
    def _load_all_data(self):
        """Load all JSON files into memory"""
        for key, filename in self.FILES.items():
            filepath = self.DATA_DIR / filename
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Handle both wrapped and unwrapped JSON structures
                    if isinstance(data, dict) and key in data:
                        self._data[key] = data[key]
                    elif isinstance(data, dict) and len(data) == 1:
                        self._data[key] = list(data.values())[0]
                    else:
                        self._data[key] = data
            except FileNotFoundError:
                self._data[key] = []
                print(f"Warning: {filename} not found. Initialized as empty.")
    
    def _save_data(self, data_type: str):
        """Save specific data type to JSON file"""
        filepath = self.DATA_DIR / self.FILES[data_type]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({data_type: self._data[data_type]}, f, indent=2, ensure_ascii=False)
    
    def get_data(self, data_type: str) -> List[Dict]:
        """Get data by type"""
        return self._data.get(data_type, [])
    
    def add_record(self, data_type: str, record: Dict):
        """Add a new record"""
        if data_type not in self._data:
            self._data[data_type] = []
        self._data[data_type].append(record)
        self._save_data(data_type)
    
    def update_record(self, data_type: str, record_id: str, updates: Dict):
        """Update existing record"""
        data = self._data.get(data_type, [])
        for i, record in enumerate(data):
            if record.get('id') == record_id:
                data[i].update(updates)
                self._save_data(data_type)
                return True
        return False
    
    def delete_record(self, data_type: str, record_id: str):
        """Delete a record"""
        data = self._data.get(data_type, [])
        self._data[data_type] = [r for r in data if r.get('id') != record_id]
        self._save_data(data_type)
    
    def query(self, data_type: str, filters: Dict = None) -> List[Dict]:
        """Query data with filters"""
        data = self._data.get(data_type, [])
        if not filters:
            return data
        
        results = []
        for record in data:
            match = True
            for key, value in filters.items():
                if key not in record or record[key] != value:
                    match = False
                    break
            if match:
                results.append(record)
        return results


@tool("get_student_profile")
def get_student_profile(student_id: str) -> str:
    """
    Get complete student profile including joined clubs and registered events.
    
    Args:
        student_id: Student's unique identifier
        
    Returns:
        Complete student profile as formatted string
    """
    db = JSONDatabase()
    
    # Get student data
    students = db.query("students", {"id": student_id})
    if not students:
        return f"Student with ID '{student_id}' not found."
    
    student = students[0]
    
    # Get joined clubs
    student_clubs = db.query("student_clubs", {"student_id": student_id})
    
    # Get registered events
    student_events = db.query("student_events", {"student_id": student_id})
    
    # Format output
    result = f"""
=== STUDENT PROFILE ===
ID: {student['id']}
Name: {student['name']}
Email: {student['email']}
Field of Study: {student['field_of_study']}
Year: {student['year']}
Interests: {', '.join(student['interests'])}
Skills: {', '.join(student['skills'])}
Profile Completed: {student['profile_completed']}
Created At: {student['created_at']}
Last Active: {student['last_active']}

=== JOINED CLUBS ({len(student_clubs)}) ===
"""
    for sc in student_clubs:
        result += f"- {sc['club_name']} (Role: {sc['role']}, Joined: {sc['joined_at'][:10]})\n"
    
    result += f"\n=== REGISTERED EVENTS ({len(student_events)}) ===\n"
    for se in student_events:
        result += f"- {se['event_title']} (Registered: {se['registered_at'][:10]})\n"
    
    return result


@tool("search_events")
def search_events(query: str = "", filters: Dict = None) -> str:
    """
    Search for events based on query and filters.
    
    Args:
        query: Natural language search query (searches in title and description)
        filters: Dict with keys like 'category', 'club_id', 'is_trending'
        
    Returns:
        List of matching events
    """
    db = JSONDatabase()
    events = db.get_data("events")
    
    results = []
    query_lower = query.lower()
    
    for event in events:
        # Text search
        if query:
            title_match = query_lower in event['title'].lower()
            desc_match = query_lower in event['description'].lower()
            tags_match = any(query_lower in tag.lower() for tag in event.get('tags', []))
            
            if not (title_match or desc_match or tags_match):
                continue
        
        # Apply filters
        if filters:
            match = True
            for key, value in filters.items():
                if key == 'date_from':
                    if event['date'] < value:
                        match = False
                        break
                elif key == 'date_to':
                    if event['date'] > value:
                        match = False
                        break
                elif key not in event or event[key] != value:
                    match = False
                    break
            if not match:
                continue
        
        results.append(event)
    
    # Format output
    if not results:
        return "No events found matching your criteria."
    
    output = f"=== FOUND {len(results)} EVENTS ===\n\n"
    for event in results:
        seats_info = f"{event['registered_count']}/{event.get('max_participants', '∞')}"
        output += f"""
📅 {event['title']}
   Club: {event['club_name']}
   Date: {event['date'][:10]} at {event['date'][11:16]}
   Location: {event['location']}
   Category: {event['category']}
   Seats: {seats_info}
   Trending: {'🔥 YES' if event.get('is_trending') else 'No'}
   Deadline: {event['registration_deadline'][:10]}
   Tags: {', '.join(event.get('tags', []))}
---
"""
    
    return output


@tool("get_club_info")
def get_club_info(club_id: str) -> str:
    """
    Get complete information about a specific club.
    
    Args:
        club_id: Club's unique identifier
        
    Returns:
        Complete club information
    """
    db = JSONDatabase()
    
    clubs = db.query("clubs", {"id": club_id})
    if not clubs:
        return f"Club with ID '{club_id}' not found."
    
    club = clubs[0]
    
    # Get club members
    members = db.query("student_clubs", {"club_id": club_id})
    
    # Get club events
    events = db.query("events", {"club_id": club_id})
    upcoming_events = [e for e in events if e['status'] == 'upcoming']
    
    result = f"""
=== CLUB INFORMATION ===
🏛️ {club['name']}

📝 Description: {club['description']}

📊 Statistics:
- Category: {club['category']}
- Members: {club['members_count']}
- Active: {'Yes' if club['is_active'] else 'No'}
- Founded: {club['created_at'][:10]}

👑 Leadership:
- President: {club['president_name']} (ID: {club['president_id']})

📚 History:
{club['history']}

✅ Requirements to Join:
"""
    for req in club['requirements']:
        result += f"- {req}\n"
    
    result += f"""
📞 Contact Information:
- Email: {club['contact_info']['email']}
- Phone: {club['contact_info']['phone']}
- Office: {club['contact_info']['office']}

🌐 Social Links:
"""
    for platform, link in club['social_links'].items():
        result += f"- {platform.capitalize()}: {link}\n"
    
    result += f"""
⏰ Meeting Schedule: {club.get('meeting_schedule', 'TBA')}
📝 Application Form: {club.get('application_form_url', 'Contact club directly')}

🎉 Upcoming Events ({len(upcoming_events)}):
"""
    for event in upcoming_events[:3]:
        result += f"- {event['title']} ({event['date'][:10]})\n"
    
    result += f"\n👥 Current Members: {len(members)}"
    
    return result


@tool("register_for_event")
def register_for_event(student_id: str, event_id: str) -> str:
    """
    Register a student for an event.
    
    Args:
        student_id: Student's ID
        event_id: Event's ID
        
    Returns:
        Registration confirmation
    """
    db = JSONDatabase()
    
    # Check if student exists
    students = db.query("students", {"id": student_id})
    if not students:
        return f"❌ Student '{student_id}' not found."
    
    # Check if event exists
    events = db.query("events", {"id": event_id})
    if not events:
        return f"❌ Event '{event_id}' not found."
    
    event = events[0]
    
    # Check if already registered
    existing = db.query("student_events", {"student_id": student_id, "event_id": event_id})
    if existing:
        return f"⚠️ You are already registered for '{event['title']}'."
    
    # Check if event is full
    if event.get('max_participants'):
        if event['registered_count'] >= event['max_participants']:
            return f"❌ Sorry, '{event['title']}' is full ({event['max_participants']}/{event['max_participants']} seats)."
    
    # Check deadline
    now = datetime.utcnow().isoformat() + "Z"
    if now > event['registration_deadline']:
        return f"❌ Registration deadline for '{event['title']}' has passed."
    
    # Register student
    registration = {
        "student_id": student_id,
        "event_id": event_id,
        "event_title": event['title'],
        "registered_at": now,
        "attended": False,
        "rating": None,
        "feedback": None
    }
    db.add_record("student_events", registration)
    
    # Update event count
    event['registered_count'] += 1
    db.update_record("events", event_id, {"registered_count": event['registered_count']})
    
    return f"""
✅ Successfully registered for '{event['title']}'!

📅 Event Details:
- Date: {event['date'][:10]} at {event['date'][11:16]}
- Location: {event['location']}
- Deadline: {event['registration_deadline'][:10]}
- Seats: {event['registered_count']}/{event.get('max_participants', '∞')}

📧 Confirmation sent to {students[0]['email']}
"""


@tool("join_club")
def join_club(student_id: str, club_id: str) -> str:
    """
    Register a student to join a club.
    
    Args:
        student_id: Student's ID
        club_id: Club's ID
        
    Returns:
        Join confirmation
    """
    db = JSONDatabase()
    
    # Check if student exists
    students = db.query("students", {"id": student_id})
    if not students:
        return f"❌ Student '{student_id}' not found."
    
    # Check if club exists
    clubs = db.query("clubs", {"id": club_id})
    if not clubs:
        return f"❌ Club '{club_id}' not found."
    
    club = clubs[0]
    
    # Check if already member
    existing = db.query("student_clubs", {"student_id": student_id, "club_id": club_id})
    if existing:
        return f"⚠️ You are already a member of '{club['name']}'."
    
    # Add membership
    membership = {
        "student_id": student_id,
        "club_id": club_id,
        "club_name": club['name'],
        "joined_at": datetime.utcnow().isoformat() + "Z",
        "role": "member",
        "is_active": True
    }
    db.add_record("student_clubs", membership)
    
    # Update club member count
    club['members_count'] += 1
    db.update_record("clubs", club_id, {"members_count": club['members_count']})
    
    return f"""
🎉 Welcome to '{club['name']}'!

You are now member #{club['members_count']}!

📧 Check your email ({students[0]['email']}) for:
- Welcome message from club president
- Next meeting details: {club.get('meeting_schedule', 'TBA')}
- Club Discord/WhatsApp group invite

📝 Application Form: {club.get('application_form_url', 'No additional form needed')}
"""


@tool("get_recommendations")
def get_recommendations(student_id: str, recommendation_type: str = "events", limit: int = 5) -> str:
    """
    Get personalized recommendations for a student.
    
    Args:
        student_id: Student's ID
        recommendation_type: Type of recommendations ('events', 'clubs', or 'all')
        limit: Maximum number of recommendations
        
    Returns:
        Personalized recommendations with explanations
    """
    db = JSONDatabase()
    
    # Get student profile
    students = db.query("students", {"id": student_id})
    if not students:
        return f"❌ Student '{student_id}' not found."
    
    student = students[0]
    student_interests = set([i.lower() for i in student['interests']])
    student_skills = set([s.lower() for s in student['skills']])
    
    recommendations = []
    
    # Event recommendations
    if recommendation_type in ["events", "all"]:
        events = db.get_data("events")
        registered_events = db.query("student_events", {"student_id": student_id})
        registered_ids = {e['event_id'] for e in registered_events}
        
        for event in events:
            if event['id'] in registered_ids:
                continue
            if event['status'] != 'upcoming':
                continue
            
            # Calculate match score
            score = 0.0
            reasons = []
            
            # Interest match
            event_tags = set([t.lower() for t in event.get('tags', [])])
            interest_match = student_interests & event_tags
            if interest_match:
                score += 0.4
                reasons.append(f"matches your interests: {', '.join(interest_match)}")
            
            # Skill match
            required_skills = set([s.lower() for s in event.get('required_skills', [])])
            skill_match = student_skills & required_skills
            if skill_match:
                score += 0.3
                reasons.append(f"you have required skills: {', '.join(skill_match)}")
            elif not required_skills:
                score += 0.3
                reasons.append("no prerequisites required")
            
            # Category match
            if event['category'].lower() in [i.lower() for i in student_interests]:
                score += 0.2
                reasons.append(f"category matches your interest")
            
            # Trending bonus
            if event.get('is_trending'):
                score += 0.1
                reasons.append("🔥 trending event!")
            
            if score > 0:
                recommendations.append({
                    "type": "event",
                    "id": event['id'],
                    "title": event['title'],
                    "club": event['club_name'],
                    "date": event['date'][:10],
                    "score": score,
                    "reasons": reasons
                })
    
    # Club recommendations
    if recommendation_type in ["clubs", "all"]:
        clubs = db.get_data("clubs")
        joined_clubs = db.query("student_clubs", {"student_id": student_id})
        joined_ids = {c['club_id'] for c in joined_clubs}
        
        for club in clubs:
            if club['id'] in joined_ids:
                continue
            if not club['is_active']:
                continue
            
            score = 0.0
            reasons = []
            
            # Interest match
            club_name_lower = club['name'].lower()
            club_desc_lower = club['description'].lower()
            
            for interest in student_interests:
                if interest in club_name_lower or interest in club_desc_lower:
                    score += 0.5
                    reasons.append(f"aligns with your interest in {interest}")
                    break
            
            # Category match
            if club['category'].lower() in [i.lower() for i in student_interests]:
                score += 0.3
                reasons.append("category matches your interests")
            
            # Popularity
            if club['members_count'] > 100:
                score += 0.2
                reasons.append(f"popular club with {club['members_count']} members")
            
            if score > 0:
                recommendations.append({
                    "type": "club",
                    "id": club['id'],
                    "title": club['name'],
                    "members": club['members_count'],
                    "score": score,
                    "reasons": reasons
                })
    
    # Sort by score
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    recommendations = recommendations[:limit]
    
    if not recommendations:
        return "No recommendations found at this time. Try updating your profile with more interests!"
    
    # Format output
    output = f"=== PERSONALIZED RECOMMENDATIONS FOR {student['name']} ===\n\n"
    
    for i, rec in enumerate(recommendations, 1):
        output += f"{i}. "
        if rec['type'] == 'event':
            output += f"📅 {rec['title']}\n"
            output += f"   Club: {rec['club']}\n"
            output += f"   Date: {rec['date']}\n"
        else:
            output += f"🏛️ {rec['title']}\n"
            output += f"   Members: {rec['members']}\n"
        
        output += f"   Match Score: {rec['score']:.0%}\n"
        output += f"   Why: {'; '.join(rec['reasons'])}\n\n"
    
    return output


@tool("update_student_profile")
def update_student_profile(student_id: str, updates: Dict) -> str:
    """
    Update student profile information.
    
    Args:
        student_id: Student's ID
        updates: Dictionary of fields to update
        
    Returns:
        Update confirmation
    """
    db = JSONDatabase()
    
    students = db.query("students", {"id": student_id})
    if not students:
        return f"❌ Student '{student_id}' not found."
    
    # Update last_active
    updates['last_active'] = datetime.utcnow().isoformat() + "Z"
    
    success = db.update_record("students", student_id, updates)
    
    if success:
        return f"✅ Profile updated successfully!\n\nUpdated fields: {', '.join(updates.keys())}"
    else:
        return "❌ Failed to update profile."


@tool("track_event_view")
def track_event_view(student_id: str, event_id: str) -> str:
    """
    Track when a student views an event (for recommendation algorithm).
    
    Args:
        student_id: Student's ID
        event_id: Event's ID
        
    Returns:
        Tracking confirmation
    """
    db = JSONDatabase()
    
    views = db.get_data("event_views")
    new_id = max([v.get('id', 0) for v in views], default=0) + 1
    
    view_record = {
        "id": new_id,
        "student_id": student_id,
        "event_id": event_id,
        "viewed_at": datetime.utcnow().isoformat() + "Z"
    }
    
    db.add_record("event_views", view_record)
    
    return "✅ Event view tracked"


@tool("save_conversation")
def save_conversation(student_id: str, agent_type: str, message: str, role: str, club_id: str = None) -> str:
    """
    Save conversation for agent memory.
    
    Args:
        student_id: Student's ID
        agent_type: Type of agent (orchestrator, club_chatbot, etc.)
        message: Message content
        role: 'user' or 'assistant'
        club_id: Optional club ID for club-specific conversations
        
    Returns:
        Save confirmation
    """
    db = JSONDatabase()
    