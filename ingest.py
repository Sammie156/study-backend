from pathlib import Path    # File System handling
from pypdf import PdfReader # Extract text from PDFs
from typing import List     # Typing hints

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

# TODO: This is very basic and very bad. It currently chunks based on text size
#       We need to chunk based on topics, headings, page and other things
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

def chunk_documents(documents):
    """
    Convert all documents into chunks
    """
    chunked_docs = []

    for doc in documents:
        text = doc["text"]
        source = doc["source"]

        chunks = chunk_text(text)

        for chunk in chunks:
            chunked_docs.append({
                "text": chunk,
                "source": source
            })

    return chunked_docs

# Testing for now
if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)

    print(f"Loaded {len(docs)} documents")
    print(f"Generated {len(chunks)} chunks")

    for i, chunk in enumerate(chunks[:5]):
        print(f"\nChunk {i+1}")
        print(chunk[:200])