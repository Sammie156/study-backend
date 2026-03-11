from ingest import load_documents, chunk_documents
from embeddings import EmbeddingService
from vector_store import VectorStore

docs = load_documents()
print("Documents Loaded: ", len(docs))

chunks = chunk_documents(docs)
print("Chunks Generated: ", len(chunks))

print("\n Example Chunk: \n")
print(chunks[0])

embedder = EmbeddingService()

texts = [chunk["text"] for chunk in chunks]
vectors = embedder.embed_documents(chunks)
print("\nEmbedding Shape:", vectors.shape)

print("\nExample Vector:\n")
print(vectors[0][:10])

vector_store = VectorStore()

chunk_texts = [c["text"] for c in chunks]
sources = [c["source"] for c in chunks]
vector_store.add_vectors(vectors, chunks)

while(True):
    query = input("Enter Query: ")

    if query == "quit":
        break

    query_vector = embedder.embed_query(query)

    results = vector_store.search(query_vector, k=3)

    print("\nSearch Results:\n")

    for r in results:
        print("Source:", r["source"])
        print(r["text"])
        print("\n---\n")