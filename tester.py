from rag_pipeline import RAGPipeline

rag = RAGPipeline()

question = input("Enter your question")
response = rag.ask(question)

print("\nAnswer:\n")
print(response["answer"])

print("\nSources:\n")
for s in response["sources"]:
    print(s["source"])