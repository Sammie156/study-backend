import logging

from fastapi import APIRouter, HTTPException

from schemas.chat import QuestionRequest
from services.rag_service import ask_question, debug_retrieval

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask")
def ask(request: QuestionRequest):
    try:
        return ask_question(request.question, k=request.k)
    except Exception as e:
        logger.error(f"Error asking question: {e}")
        raise HTTPException(status_code=500, detail="Failed to process question")


@router.post("/debug/retrieval")
def debug(request: QuestionRequest):
    try:
        return debug_retrieval(request.question, k=request.k)
    except Exception as e:
        logger.error(f"Error debugging retrieval: {e}")
        raise HTTPException(status_code=500, detail=str(e))
