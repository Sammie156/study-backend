from fastapi import APIRouter
from schemas.chat import QuestionRequest
from services.rag_service import ask_question, debug_retrieval

router = APIRouter()

@router.post("/ask")
def ask(request: QuestionRequest):
    return ask_question(request.question)

@router.post("/debug/retrieval")
def debug(request: QuestionRequest):
    return debug_retrieval(request.question)