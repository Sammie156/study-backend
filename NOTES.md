# Notes. Stuff. Something

Alright. First the files and what each does.

| File              | Purpose                                                |
| ----------------- | ------------------------------------------------------ |
| `ingest.py`       | Extract text from PDFs and convert them into chunks    |
| `embeddings.py`   | Generate embeddings of the chunks created in ingest.py |
| `vector_store.py` | Manage FAISS                                           |
| `rag_pipeline.py` | Answer Questions                                       |
| `config.py`       | If any specific config is needed for the LLM           |

## `ingest.py`

This file scans all the PDFs and materials(currently only PDFs) present inside `data\` folder and extracts the text from them. Then after extracting the text from all the documents, it chunks them based on token size, and stores all the chunks into a single list.
