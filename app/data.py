from models import (
    get_session, init_db, Student, StudentProfile, Club, Event, Skill
)
from datetime import datetime, timedelta
import random

def populate_sample_data():
    """Populate database with sample data"""
    print("🚀 Initializing database...")
    init_db()
    
    session = get_session()
    
    try:
        # Create Skills
        print("📚 Creating skills...")
        skills_data = [
            ("Python", "technical"),
            ("JavaScript", "technical"),
            ("Java", "technical"),
            ("C++", "technical"),
            ("React", "technical"),
            ("Node.js", "technical"),
            ("TensorFlow", "technical"),
            ("Docker", "technical"),
            ("SQL", "technical"),
            ("Git", "technical"),
            ("Machine Learning", "technical"),
            ("Data Analysis", "technical"),
            ("UI/UX Design", "technical"),
            ("Leadership", "soft_skill"),
            ("Teamwork", "soft_skill"),
            ("Communication", "soft_skill"),
            ("Problem Solving", "soft_skill"),
            ("Project Management", "soft_skill"),
            ("Public Speaking", "soft_skill"),
            ("French", "language"),
            ("Spanish", "language"),
            ("Arabic", "language"),
            ("English", "language")
        ]
        
        skills = []
        for name, category in skills_data:
            skill = Skill(name=name, category=category)
            skills.append(skill)
            session.add(skill)
        session.commit()
        print(f"   ✅ Created {len(skills)} skills")
        
        # Create Clubs
        print("🎯 Creating clubs...")
        clubs_data = [
            {
                "name": "AI & Machine Learning Club",
                "description": "Exploring artificial intelligence and machine learning technologies through workshops, projects, and competitions",
                "mission": "To foster a community of AI enthusiasts and practitioners who push the boundaries of intelligent systems",
                "history": "Founded in 2018 by a group of computer science students passionate about AI. We've since organized 50+ workshops and 10 hackathons.",
                "contact_email": "ai.club@university.edu",
                "website": "https://aiclub.university.edu",
                "personality_style": "tech-focused"
            },
            {
                "name": "Web Development Society",
                "description": "Building awesome websites and web applications using modern technologies and best practices",
                "mission": "To help students learn modern web development technologies and build real-world projects",
                "history": "Established in 2015, we've helped hundreds of students build their first websites and launch successful web careers.",
                "contact_email": "webdev@university.edu",
                "website": "https://webdev.university.edu",
                "personality_style": "casual"
            },
            {
                "name": "Entrepreneurship Club",
                "description": "Turning innovative ideas into successful businesses through mentorship, workshops, and networking",
                "mission": "To support student entrepreneurs in launching their startups and developing business skills",
                "history": "Started in 2016 with 10 members, now over 200 strong. Our members have launched 15 successful startups.",
                "contact_email": "entrepreneurs@university.edu",
                "website": "https://entrepreneurship.university.edu",
                "personality_style": "professional"
            },
            {
                "name": "Robotics Team",
                "description": "Designing, building, and programming robots for competitions and real-world applications",
                "mission": "To compete in national robotics competitions and inspire the next generation of engineers",
                "history": "Winner of 5 regional championships since 2017. Our robots have competed internationally.",
                "contact_email": "robotics@university.edu",
                "website": "https://robotics.university.edu",
                "personality_style": "enthusiastic"
            },
            {
                "name": "Design Collective",
                "description": "Creative designers working on visual design, UX/UI, and innovative projects",
                "mission": "To cultivate design thinking and creative problem-solving skills",
                "history": "Formed in 2019 by graphic design and HCI students. We've completed 30+ client projects.",
                "contact_email": "design@university.edu",
                "website": "https://design.university.edu",
                "personality_style": "creative"
            },
            {
                "name": "Cybersecurity Club",
                "description": "Learning and practicing cybersecurity skills through CTF competitions and workshops",
                "mission": "To develop cybersecurity awareness and skills among students",
                "history": "Founded in 2020, we participate in national CTF competitions and organize security workshops.",
                "contact_email": "security@university.edu",
                "website": "https://security.university.edu",
                "personality_style": "tech-focused"
            }
        ]
        
        clubs = []
        for club_data in clubs_data:
            club = Club(**club_data)
            clubs.append(club)
            session.add(club)
        session.commit()
        print(f"   ✅ Created {len(clubs)} clubs")
        
        # Create Events
        print("📅 Creating events...")
        event_types = ["workshop", "hackathon", "competition", "social", "seminar", "networking"]
        event_templates = {
            "workshop": ["Hands-on", "Introduction to", "Advanced", "Practical"],
            "hackathon": ["24-Hour", "Weekend", "Innovation", "Code"],
            "competition": ["Annual", "Inter-University", "Challenge", "Championship"],
            "social": ["Meetup", "Networking", "Social", "Get-Together"],
            "seminar": ["Tech Talk", "Guest Speaker", "Industry Insights", "Career"],
            "networking": ["Industry", "Alumni", "Professional", "Career"]
        }
        
        events_created = 0
        for i, club in enumerate(clubs):
            for j in range(6):  # 6 events per club
                days_ahead = (i * 6 + j + 1) * 5 + random.randint(0, 10)
                event_date = datetime.utcnow() + timedelta(days=days_ahead)
                deadline = event_date - timedelta(days=random.randint(2, 7))
                
                event_type = random.choice(event_types)
                template = random.choice(event_templates[event_type])
                
                event = Event(
                    club_id=club.id,
                    title=f"{template} {event_type.capitalize()}: {club.name.split()[0]} Edition",
                    description=f"Join us for an exciting {event_type} organized by {club.name}. This event will provide hands-on experience and networking opportunities. Perfect for students interested in {club.name.lower()}.",
                    event_type=event_type,
                    location=random.choice(["Building A - Room 101", "Main Auditorium", "Computer Lab 3", "Online (Zoom)", "Campus Center", "Innovation Hub"]),
                    date=event_date,
                    deadline=deadline,
                    max_seats=random.choice([30, 50, 75, 100, 150, None]),
                    current_registrations=random.randint(5, 40),
                    is_trending=random.random() > 0.6,
                    view_count=random.randint(20, 800)
                )
                
                # Assign relevant skills to events
                relevant_skills = []
                if "AI" in club.name or "Machine Learning" in club.name:
                    relevant_skills = [s for s in skills if s.name in ["Python", "TensorFlow", "Machine Learning", "Data Analysis"]]
                elif "Web" in club.name:
                    relevant_skills = [s for s in skills if s.name in ["JavaScript", "React", "Node.js", "HTML", "CSS"]]
                elif "Robotics" in club.name:
                    relevant_skills = [s for s in skills if s.name in ["Python", "C++", "Git"]]
                elif "Design" in club.name:
                    relevant_skills = [s for s in skills if s.name in ["UI/UX Design", "Communication"]]
                else:
                    relevant_skills = random.sample(skills, k=random.randint(2, 4))
                
                event.required_skills = random.sample(relevant_skills, k=min(3, len(relevant_skills)))
                session.add(event)
                events_created += 1
        
        session.commit()
        print(f"   ✅ Created {events_created} events")
        
        # Create Students
        print("👥 Creating students...")
        fields_of_study = ["Computer Science", "Software Engineering", "Data Science", "Business Administration", "Design", "Electrical Engineering"]
        student_names = [
            "Ahmed Ben Ali", "Sara Mansouri", "Mohamed Trabelsi", "Leila Kacem",
            "Youssef Ben Salem", "Amira Gharbi", "Nabil Sfaxi", "Rania Ben Ahmed",
            "Karim Bouazizi", "Nour El Houda Mejri", "Amine Jebali", "Sana Zaouali",
            "Mehdi Ben Salah", "Yasmine Hamdi", "Khalil Cherif", "Ines Bouzid",
            "Omar Triki", "Salma Ghariani", "Fares Souissi", "Marwa Ben Amor"
        ]
        
        students = []
        for i, name in enumerate(student_names):
            email = name.lower().replace(" ", ".") + "@student.university.edu"
            field = random.choice(fields_of_study)
            
            student = Student(
                name=name,
                email=email,
                field_of_study=field,
                year_level=random.randint(1, 4)
            )
            
            # Add profile
            profile = StudentProfile(
                student=student,
                bio=f"Hi! I'm {name}, a passionate {field} student. I love learning new technologies and working on innovative projects.",
                goals="Build impactful projects, expand my network, and develop both technical and soft skills",
                notification_preferences='{"email": true, "push": true, "weekly_digest": true}'
            )
            
            # Assign skills based on field of study
            student_skills = []
            if "Computer" in field or "Software" in field:
                student_skills = random.sample([s for s in skills if s.category == "technical"], k=random.randint(4, 8))
            elif "Data Science" in field:
                student_skills = [s for s in skills if s.name in ["Python", "SQL", "Machine Learning", "Data Analysis"]]
            elif "Design" in field:
                student_skills = [s for s in skills if s.name in ["UI/UX Design", "Communication", "Problem Solving"]]
            else:
                student_skills = random.sample(skills, k=random.randint(3, 6))
            
            # Add some soft skills
            soft_skills = random.sample([s for s in skills if s.category == "soft_skill"], k=random.randint(2, 4))
            student.skills = student_skills + soft_skills
            
            # Join random clubs (1-3 clubs per student)
            student.clubs = random.sample(clubs, k=random.randint(1, 3))
            
            students.append(student)
            session.add(student)
            session.add(profile)
        
        session.commit()
        print(f"   ✅ Created {len(students)} students")
        
        # Register students for events
        print("🎟️  Registering students for events...")
        all_events = session.query(Event).all()
        registrations = 0
        
        for student in students:
            # Students in clubs more likely to register for their club's events
            club_events = [e for e in all_events if e.club in student.clubs]
            other_events = [e for e in all_events if e.club not in student.clubs]
            
            # Register for 2-4 events from their clubs
            events_to_register = random.sample(club_events, k=min(random.randint(2, 4), len(club_events)))
            
            # Register for 1-2 events from other clubs
            events_to_register += random.sample(other_events, k=min(random.randint(1, 2), len(other_events)))
            
            for event in events_to_register:
                if event not in student.registered_events and not event.is_full:
                    student.registered_events.append(event)
                    registrations += 1
        
        session.commit()
        print(f"   ✅ Created {registrations} event registrations")
        
        print("\n" + "="*60)
        print("✅ DATABASE POPULATED SUCCESSFULLY!")
        print("="*60)
        print(f"📊 Summary:")
        print(f"   • Skills: {len(skills)}")
        print(f"   • Clubs: {len(clubs)}")
        print(f"   • Events: {events_created}")
        print(f"   • Students: {len(students)}")
        print(f"   • Event Registrations: {registrations}")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error populating data: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    populate_sample_data()