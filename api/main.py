import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import chat

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


app = FastAPI()

origins = [
    "http://localhost:3000",  # Next.js frontend will run here, so....
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Only for development
    allow_headers=["*"],  # Only for development
)

app.include_router(chat.router)


@app.get("/")
def health_check():
    return {"status": "Study Copilot is alive"}
