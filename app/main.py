
from api.routers.agents import chat, master, recommendations, search 
from api.routers.autontification import auth
from api.routers.student import student
from api.routers.club import club
from api.routers.events import  events
from api.routers.skills import skills
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000/",
        "https://club-student-hub.vercel.app/", 
        "https://sys-multi-agents.onrender.com/",
        ""
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(master.router)
app.include_router(recommendations.router)
app.include_router(search.router)
app.include_router(auth.router)
app.include_router(student.router)
app.include_router(club.router)
app.include_router(events.router)
app.include_router(skills.router)





