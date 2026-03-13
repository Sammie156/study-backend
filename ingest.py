from pathlib import Path    # File System handling
from pypdf import PdfReader # Extract text from PDFs
from typing import List     # Typing hints

from embeddings import EmbeddingService
from vector_store import VectorStore

DATA_DIR = Path("data")

def get_pdf_files() -> List[Path]:
    """
    Get all the PDF files inside the data directory
    """
    return list(DATA_DIR.glob("*.pdf"))

def extract_pdf(file_path: Path) -> str:
    """
    Extract the text from a single PDF
    """
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    
    return text

def load_documents() -> List[str]:
    """
    Load all the documents and extract the PDFs and
    compile into one single text
    """
    pdf_files = get_pdf_files()

    documents = []

    for pdf in pdf_files:
        text = extract_pdf(pdf)
        documents.append({
            "text": text,
            "source": pdf.name
        })

    return documents

# FIXME: This needs to changed to chunk_paragraphs().
#        Let us have this function for now, for learning, but
#        we are currently using chunk_paragraph()
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """
    Split the text into overlapping chunks
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        
        chunks.append(chunk)

        start += chunk_size - overlap
    
    return chunks

def chunk_paragraph(text: str, chunk_size: int = 500, overlap: int = 50):
    """
    Paragraph-aware chunking.
    Slightly better, but still could be much better.
    """
    paragraphs = text.split("\n\n")

    paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 40]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        
        if len(current_chunk) + len(paragraph) > chunk_size:
            chunks.append(current_chunk.strip())

            current_chunk = current_chunk[-overlap:] + " "
        
        current_chunk += paragraph + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def chunk_documents(documents):
    """
    Convert all documents into chunks
    """
    chunked_docs = []

    for doc in documents:
        text = doc["text"]
        source = doc["source"]

        chunks = chunk_paragraph(text)

        for chunk in chunks:
            chunked_docs.append({
                "text": chunk,
                "source": source
            })

    return chunked_docs

# THE INGESTION PIPELINE!
if __name__ == "__main__":
    print("Starting Ingestion Pipeline")

    documents = load_documents()
    print("Documents Loaded: ", len(documents))

    chunks = chunk_documents(documents)
    print("Chunks created: ", len(chunks))

    texts = [chunk["text"] for chunk in chunks]

    embedder = EmbeddingService()
    vectors = embedder.embed_documents(texts)

    vector_store = VectorStore()
    vector_store.add_vectors(vectors, chunks)

    vector_store.save()

    print("FAISS index built successfully!")