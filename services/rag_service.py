from rag_pipeline import RAGPipeline

rag_pipeline = RAGPipeline()

def format_sources(chunks):
    formatted_sources = []

    for chunk in chunks:
        preview = chunk["text"][:200].replace("\n", " ").strip()

        formatted_sources.append({
            "source": chunk["source"],
            "preview": preview + "..."
        })
    
    return formatted_sources

def debug_retrieval(question: str):
    contexts = rag_pipeline.retrieve_context(question)

    return {
        "question": question,
        "retrieved_chunks": contexts
    }

def ask_question(question: str):
    response = rag_pipeline.ask(question)

    formatted_sources = format_sources(response["sources"])

    return {
        "question": question,
        "answer": response["answer"],
        "sources": formatted_sources,
        "retrieved_chunks": response["sources"] # for debugging at the moment
    }
