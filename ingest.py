import logging
from pathlib import Path  # File System handling
from typing import List  # Typing hints

from pypdf import PdfReader  # Extract text from PDFs

from embeddings import EmbeddingService
from vector_store import VectorStore

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

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
        documents.append({"text": text, "source": pdf.name})

    return documents


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
            chunked_docs.append({"text": chunk, "source": source})

    return chunked_docs


# THE INGESTION PIPELINE!
if __name__ == "__main__":
    logger.info("Starting Ingestion Pipeline")

    documents = load_documents()
    logger.info("Documents Loaded: %s", len(documents))

    chunks = chunk_documents(documents)
    logger.info("Chunks created: %s", len(chunks))

    texts = [chunk["text"] for chunk in chunks]

    embedder = EmbeddingService()
    vectors = embedder.embed_documents(texts)

    vector_store = VectorStore()
    vector_store.add_vectors(vectors, chunks)

    vector_store.save()

    logger.info("FAISS index built successfully!")
