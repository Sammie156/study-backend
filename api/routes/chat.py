from fastapi import APIRouter
from schemas.chat import QuestionRequest
from services.rag_service import ask_question

router = APIRouter()

@router.post("/ask")
def ask(request: QuestionRequest):
    return ask_question(request.question)