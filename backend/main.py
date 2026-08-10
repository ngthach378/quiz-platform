from fastapi import FastAPI

app = FastAPI(
    title="Quiz Platform API",
    description="API for the Quiz Platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Quiz Platform API is running",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }