from fastapi import FastAPI

from backend.routers.users import router as users_router
from backend.routers.exams import router as exams_router


app = FastAPI(
    title="Quiz Platform API",
    description="API for the Quiz Platform",
    version="0.1.0",
)


app.include_router(users_router)
app.include_router(exams_router)


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