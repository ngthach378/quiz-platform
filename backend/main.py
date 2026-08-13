from fastapi import FastAPI

from backend.routers.users import router as users_router
from backend.routers.exams import router as exams_router
from backend.routers.questions import router as questions_router
from backend.routers.question_options import (
    router as question_options_router,
)
from backend.routers.question_statements import (
    router as question_statements_router,
)
from backend.routers.numeric_answers import (
    router as numeric_answers_router,
)
from backend.routers.exam_questions import (
    router as exam_questions_router,
)
from backend.routers.attempts import router as attempts_router

app = FastAPI(
    title="Quiz Platform API",
    description="API for the Quiz Platform",
    version="0.1.0",
)


app.include_router(users_router)
app.include_router(exams_router)
app.include_router(questions_router)
app.include_router(question_options_router)
app.include_router(question_statements_router)
app.include_router(numeric_answers_router)
app.include_router(exam_questions_router)
app.include_router(attempts_router)

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