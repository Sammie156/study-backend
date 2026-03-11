import faiss                # FAISS stuff, vector databases...
import numpy as np          # Numpy...
import json                 # Storing metadata
from pathlib import Path    # Filesystem handling

INDEX_DIR = Path("data/index")
INDEX_DIR.mkdir(parents=True, exist_ok=True)

INDEX_FILE = INDEX_DIR / "faiss_index.bin"
METADATA_FILE = INDEX_DIR / "metadata.json"

class VectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension # 384 as we use MiniLM model
        self.index = faiss.IndexFlatIP(dimension)
        self.metadata = []

    def add_vectors(self, vectors: np.ndarray, chunks: list):
        """
        Add embeddings and metadata to the index
        """
        faiss.normalize_L2(vectors)
        self.index.add(vectors)

        for chunk in chunks:
            self.metadata.append(chunk)
    
    def search(self, query_vector: np.ndarray, k: int = 5):
        """
        Search the FAISS index for the most similar vectors
        """
        query_vector = np.array([query_vector])

        faiss.normalize_L2(query_vector)

        distances, indices = self.index.search(query_vector, k)

        results = []

        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        
        return results
    
    def save(self):
        """
        Save the FAISS index and metadata
        """

        faiss.write_index(self.index, str(INDEX_FILE))

        with open(METADATA_FILE, "w") as f:
            json.dump(self.metadata, f)
    
    def load(self):
        """
        Load the FAISS index and metadata
        """

        if INDEX_FILE.exists():
            self.index = faiss.read_index(str(INDEX_FILE))
        
        if METADATA_FILE.exists():
            with open(METADATA_FILE, "r") as f:
                self.metadata = json.load(f)