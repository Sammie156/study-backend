import logging
from mimetypes import knownfiles

from rag_pipeline import RAGPipeline

logger = logging.getLogger(__name__)

rag_pipeline = RAGPipeline()


def format_sources(chunks):
    formatted_sources = []

    for chunk in chunks:
        preview = chunk["text"][:200].replace("\n", " ").strip()

        formatted_sources.append(
            {"source": chunk["source"], "preview": preview + "..."}
        )

    return formatted_sources


def debug_retrieval(question: str, k: int = 5):
    try:
        response = rag_pipeline.retrieve_context(question, k=k)
        return {"question": question, "retrieved_chunks": response}
    except Exception as e:
        logger.error(f"Error debugging retrieval: {e}")
        raise


def ask_question(question: str, k: int = 5):
    try:
        response = rag_pipeline.ask(question, k=k)
        return {
            "question": question,
            "answer": response["answer"],
            "sources": format_sources(response["sources"]),
        }
    except Exception as e:
        logger.error("ask_question failed: %s", e)
        raise
