from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline import RAGPipeline

app = FastAPI()

rag_pipeline = RAGPipeline()

class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def health_check():
    return {"status": "Study Copilot is alive"}


@app.post("/ask")
def ask_question(request: QuestionRequest):

    response = rag_pipeline.ask(request.question)

    return {
        "question": request.question,
        "answer": response["answer"],
        "sources": response["sources"]
    }