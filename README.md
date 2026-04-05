# Study Copilot – RAG Backend

A Retrieval-Augmented Generation (RAG) backend for an AI-powered study assistant. Upload your study material (PDFs, notes) and ask questions — the system retrieves the most relevant chunks and generates accurate, source-cited answers using Google Gemini.

## How It Works

1. **Ingest** – Documents are loaded, split into overlapping text chunks, and stored
2. **Embed** – Each chunk is converted into a vector using `all-MiniLM-L6-v2` (sentence-transformers)
3. **Store** – Vectors are saved to a local vector store for fast similarity search
4. **Query** – At query time, the question is embedded and the top-k most relevant chunks are retrieved
5. **Generate** – Retrieved context is passed to Gemini with a structured prompt; the answer is returned with source citations

## Project Structure

| File | Purpose |
|------|---------|
| `main.py` | Entry point |
| `ingest.py` | Document loading and chunking |
| `embeddings.py` | Embedding service using sentence-transformers |
| `vector_store.py` | Vector storage and cosine similarity search |
| `rag_pipeline.py` | Core RAG loop — retrieval, prompt building, generation |
| `tester.py` | Manual test runner |
| `config.py` | API keys and configuration |

## Setup
```bash
git clone https://github.com/Sammie156/study-backend
cd study-backend
pip install -r requirements.txt
```

Add your Gemini API key to `config.py`:
```python
GEMINI_API_KEY = "your-key-here"
```

Then ingest your documents and start querying:
```bash
python ingest.py        # load and embed your study material
python main.py          # start asking questions
```

## Tech Stack

- **Python** – Core language
- **sentence-transformers** – Local text embeddings (`all-MiniLM-L6-v2`)
- **Google Gemini API** – Answer generation (`gemini-2.5-flash`)
- **NumPy** – Vector operations and similarity search

## Known Limitations

- Chunking is currently size-based with overlap; semantic/heading-aware chunking is planned
- Vector store is file-based (no persistent DB like FAISS or ChromaDB yet)

## Roadmap

- [ ] Semantic chunking (by headings, topics, pages)
- [ ] Swap file-based store for FAISS or ChromaDB
- [ ] REST API wrapper (FastAPI) for frontend integration
- [ ] Multi-document session support
