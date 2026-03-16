from rag_pipeline import RAGPipeline

rag_pipeline = RAGPipeline()

def ask_question(question: str):
    response = rag_pipeline.ask(question)

    return {
        "question": question,
        "answer": response["answer"],
        "sources": response["sources"]
    }