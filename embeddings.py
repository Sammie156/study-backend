from sentence_transformers import SentenceTransformer   # EMBEDDING MODELL!!!
import numpy as np                                      # For vector arrays
from typing import List                                 # Hints

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the Embedding model and have it available in the memory
        """
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a batch of documents
        """
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True
        )

        return np.array(embeddings)
    
    def embed_query(self, query: str) -> np.ndarray:
        """
        Generate embeddings for a single query
        """
        embedding = self.model.encode(query)

        return np.array(embedding)
