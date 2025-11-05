
from api.routers.agents import chat, master, recommendations, search 
from api.routers.autontification import auth
from fastapi import FastAPI





app = FastAPI()

app.include_router(chat.router)
app.include_router(master.router)
app.include_router(recommendations.router)
app.include_router(search.router)
app.include_router(auth.router)





