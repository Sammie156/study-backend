from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Student Copilot Backend is running"}