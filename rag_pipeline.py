from google import genai
from embeddings import EmbeddingService
from vector_store import VectorStore
from config import GEMINI_API_KEY


class RAGPipeline:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.vector_store = VectorStore()

        self.vector_store.load()

        self.client = genai.Client(api_key=GEMINI_API_KEY)
    
    def retrieve_context(self, query, k=5):
        query_vector = self.embedder.embed_query(query)

        results = self.vector_store.search(query_vector, k)

        return results

    def build_prompt(self, query, contexts):
        """
        Prompt engineering
        """
        context_text = "\n\n".join([c["text"] for c in contexts])

        prompt = f"""
You are a helpful AI assistant.

Use the following study material to answer the question.

Context:
{context_text}

Question:
{query}

Answer clearly and cite the material when relevant. 
Moreover, make the answers structured and understandable with no need to refer the PDF sources.
"""

        return prompt
    
    def generate_answer(self, prompt):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-lite", # I keep changing this depending on Google's mood
            contents=prompt
        )

        return response.text
    
    def ask(self, question):
        contexts = self.retrieve_context(question)

        prompt = self.build_prompt(question, contexts)

        answer = self.generate_answer(prompt)

        return {
            "answer": answer,
            "sources": contexts
        }