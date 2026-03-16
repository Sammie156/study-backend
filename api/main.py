from fastapi import FastAPI
from api.routes import chat

app = FastAPI()

app.include_router(chat.router)

@app.get("/")
def health_check():
    return {"status": "Study Copilot is alive"}