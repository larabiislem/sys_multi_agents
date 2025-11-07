# GCL Backend + Multi-Agent System 🤖⚡

A powerful backend system integrated with sophisticated multi-agent AI architecture built using CrewAI that powers the ClubEvent-Hub platform. This system provides intelligent automation for student club discovery, event recommendations, and personalized interactions through specialized AI agents with robust backend infrastructure.

## 🚀 Overview

The GCL Backend + Multi-Agent System combines advanced AI capabilities powered by CrewAI to revolutionize how students interact with university clubs and events. The system features a scalable backend architecture with multiple specialized AI agents working in harmony to provide personalized, intelligent assistance.

## 📊 API Documentation

The interactive API documentation is available here: https://sys-multi-agents.onrender.com/docs

## 🏗️ System Architecture

### Backend Infrastructure
- **FastAPI Framework**: High-performance REST API backend
- **Database Layer**: SQLAlchemy ORM with PostgreSQL integration
- **Authentication System**: Secure user verification and session management
- **Cloud Deployment**: Render.com integration for scalable hosting

### Multi-Agent System (Built with CrewAI)

The multi-agent architecture leverages CrewAI's powerful framework to orchestrate intelligent AI agents that work collaboratively to serve students' needs.

#### 🎯 Master Orchestrator Agent
The central control unit built with CrewAI that manages the entire system:
- **Request Routing**: Intelligently directs student queries to appropriate specialized agents
- **Context Management**: Maintains conversation state across multiple interactions
- **Load Balancing**: Distributes workload across available agent instances
- **Error Handling**: Provides fallback responses when specialized agents are unavailable
- **Performance Monitoring**: Tracks system metrics and agent response times
- **CrewAI Integration**: Leverages CrewAI's orchestration capabilities for seamless agent coordination

#### 💬 Club Chatbot Agents
Dedicated AI assistants for each university club, powered by CrewAI:
- **24/7 Availability**: Instant responses replacing delayed WhatsApp communications
- **Club Expertise**: Comprehensive knowledge of club history, members, events, and requirements
- **Personality Matching**: Each bot reflects the unique culture and style of its respective club
- **Application Assistance**: Step-by-step guidance through membership processes
- **Conversation Memory**: Persistent chat history for seamless user experience
- **CrewAI Agent Framework**: Built using CrewAI's agent architecture for consistent behavior

#### 🎯 Smart Recommendation Agent
Advanced personalization engine powered by machine learning and CrewAI:
- **Profile Analysis**: Deep evaluation of student interests, academic focus, and skill sets
- **Behavioral Learning**: Real-time analysis of platform interactions and preferences
- **Pattern Recognition**: Identifies opportunities based on similar student profiles
- **Temporal Intelligence**: Considers academic calendars, exam periods, and project deadlines
- **Personalized Feeds**: Weekly curated content with detailed reasoning for each recommendation
- **CrewAI ML Integration**: Utilizes CrewAI's machine learning capabilities for enhanced recommendations

#### 🔍 Event Discovery and Search Agent
Natural language processing for advanced search capabilities, built with CrewAI:
- **Conversational Search**: Understands queries like "show me AI events this month"
- **Semantic Understanding**: Recognizes synonyms and related terms across different contexts
- **Multi-Criteria Filtering**: Advanced filtering by date, location, club, skills, and availability
- **Trending Analysis**: Real-time identification of popular events and limited-capacity opportunities
- **Smart Suggestions**: Proactive recommendations based on search patterns
- **CrewAI NLP**: Powered by CrewAI's natural language processing capabilities

#### 🚀 Onboarding and Profile Builder Agent
Intelligent user lifecycle management using CrewAI:
- **Guided Onboarding**: Interactive questionnaire system for new user setup
- **Instant Value Delivery**: Immediate club and event suggestions upon registration
- **Dynamic Profiling**: Continuous profile updates based on user activities and feedback
- **Preference Management**: Granular control over notifications and communication settings
- **Growth Tracking**: Adaptive recommendations as student interests and skills evolve
- **CrewAI Workflow**: Leverages CrewAI's workflow management for smooth user journeys

## 🛠️ Technical Stack

- **Backend Framework**: FastAPI with Python 3.11+
- **Multi-Agent Framework**: CrewAI for intelligent agent coordination
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based verification system
- **Deployment**: Render.com with automated CI/CD
- **Language Composition**: 100% Python

## 📁 Project Structure

```
sys_multi_agents/
├── app/
│   ├── api/                    # REST API endpoints and routing logic
│   ├── models/                 # Database models and Pydantic schemas
│   ├── multi_agents/          # CrewAI-powered multi-agent system implementations
│   │   ├── orchestrator.py    # Master orchestrator agent (CrewAI)
│   │   ├── club_chatbots/     # Individual club chatbot agents (CrewAI)
│   │   ├── recommendation.py  # Smart recommendation engine (CrewAI)
│   │   ├── discovery.py       # Event discovery and search agent (CrewAI)
│   │   ├── onboarding.py      # Profile builder and onboarding agent (CrewAI)
│   │   └── crew_config.py     # CrewAI configuration and setup
│   ├── database.py            # Database configuration and connection
│   ├── main.py               # FastAPI application entry point
│   ├── verify.py             # Authentication and user verification
│   ├── requirements.txt      # Python package dependencies (includes CrewAI)
│   ├── runtime.txt          # Python version specification (3.11)
│   └── render.yaml          # Cloud deployment configuration
├── .gitignore               # Version control exclusions
└── README.md               # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 12+
- Git
- Virtual environment (recommended)
- CrewAI API access (if using cloud features)

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ClubEvent-Hub/sys_multi_agents.git
   cd sys_multi_agents
   ```

2. **Environment Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   cd app
   pip install -r requirements.txt
   ```

3. **Launch the System**
   ```bash
   # Start the backend server
   python main.py
   
   # Alternative: Use uvicorn directly
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

The system will be accessible at `http://localhost:8000`

## 🔧 Configuration

### Environment Variables
```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/db_name
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30

# Security
SECRET_KEY=your-super-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG_MODE=False

# CrewAI Configuration
CREWAI_API_KEY=your-crewai-api-key
CREWAI_MODEL=gpt-4
CREWAI_TEMPERATURE=0.7
CREW_MAX_AGENTS=10

# Agent Configuration
MAX_CONCURRENT_AGENTS=10
AGENT_TIMEOUT_SECONDS=30
CONTEXT_MEMORY_SIZE=1000

# External Services
OPENAI_API_KEY=your-openai-key
RENDER_API_KEY=your-render-key
```

## 📊 Key Features

### Backend Capabilities
- **High-Performance API**: FastAPI-based REST endpoints with automatic documentation
- **Scalable Architecture**: Microservices design supporting horizontal scaling
- **Real-time Processing**: WebSocket support for live interactions
- **Comprehensive Logging**: Detailed analytics and performance monitoring
- **Security First**: JWT authentication with role-based access control

### CrewAI-Powered Multi-Agent Intelligence
- **Contextual Understanding**: Natural language processing across all interactions
- **Learning Capabilities**: Machine learning models that improve over time powered by CrewAI
- **Fault Tolerance**: Graceful degradation when individual agents are unavailable
- **Load Distribution**: Intelligent workload balancing across CrewAI agent instances
- **Memory Persistence**: Long-term conversation and interaction history
- **Agent Collaboration**: CrewAI's framework enables seamless inter-agent communication

## 🔐 Security

- **Authentication**: JWT-based token system with refresh capabilities
- **Authorization**: Role-based permissions for different user types
- **Data Protection**: Encryption at rest and in transit
- **Input Validation**: Comprehensive request validation and sanitization
- **Rate Limiting**: API throttling to prevent abuse
- **CrewAI Security**: Secure API key management for CrewAI services

## 📈 Performance & Scaling

- **Horizontal Scaling**: Multi-instance deployment support
- **Caching Layer**: Redis integration for improved response times
- **Database Optimization**: Connection pooling and query optimization
- **Monitoring**: Prometheus metrics and Grafana dashboards
- **Auto-scaling**: Cloud-native scaling based on demand
- **CrewAI Optimization**: Efficient agent resource utilization

## 🤝 Contributing

We welcome contributions to enhance the GCL Backend + Multi-Agent System:

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-enhancement`
3. **Commit Changes**: `git commit -m 'Add amazing enhancement'`
4. **Push Branch**: `git push origin feature/amazing-enhancement`
5. **Submit Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Include comprehensive tests for new features
- Update documentation for API changes
- Ensure backward compatibility
- Test CrewAI agent integrations thoroughly

## 🙏 Acknowledgments

This project is built using the powerful **CrewAI** framework for multi-agent orchestration. Special thanks to the CrewAI team for providing the foundational technology that makes our intelligent agent system possible.

- **CrewAI**: [https://crewai.com](https://crewai.com)
- **FastAPI**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **PostgreSQL**: [https://postgresql.org](https://postgresql.org)
