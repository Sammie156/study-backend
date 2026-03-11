from pathlib import Path    # File System handling
from pypdf import PdfReader # Extract text from PDFs
from typing import List     # Typing hints

DATA_DIR = Path("data")

# Get all the PDF files inside the data directory
def get_pdf_files() -> List[Path]:
    # Basically scan the directory where data is stored
    # And then return a list of all PDFs' path there
    return list(DATA_DIR.glob("*.pdf"))

# Extract the text from a single PDF
def extract_pdf(file_path: Path) -> str:
    # Configuring PDF reader
    reader = PdfReader(file_path)

    text = ""

    # Take the text from all the pages and then print them
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    
    return text

# Run all the above functions
def load_documents() -> List[str]:
    pdf_files = get_pdf_files()

    documents = []

    for pdf in pdf_files:
        text = extract_pdf(pdf)
        documents.append(text)

    return documents

# Testing for now
if __name__ == "__main__":
    docs = load_documents()

    print(f"Loaded {len(docs)} documents")

    for i, doc in enumerate(docs):
        print(f"\nDocument {i+1} preview:")
        print(doc[:500])