
from api.routers.agents import chat, master, recommendations, search
from fastapi import FastAPI





app = FastAPI()

app.include_router(chat.router)
app.include_router(master.router)
app.include_router(recommendations.router)
app.include_router(search.router)





