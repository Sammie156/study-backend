from rag_pipeline import RAGPipeline

rag = RAGPipeline()

response = rag.ask("What is data coupling and stamp coupling?")

print("\nAnswer:\n")
print(response["answer"])

print("\nSources:\n")
for s in response["sources"]:
    print(s["source"])