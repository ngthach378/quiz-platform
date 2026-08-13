from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.question import Question
from backend.schemas.question import QuestionCreate, QuestionResponse


router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@router.post("/", response_model=QuestionResponse)
def create_question(
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
):
    question = Question(
        content=question_data.content,
        question_type=question_data.question_type,
        explanation=question_data.explanation,
        difficulty=question_data.difficulty,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    return question


@router.get("/", response_model=list[QuestionResponse])
def get_questions(
    db: Session = Depends(get_db),
):
    return db.query(Question).all()


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
):
    question = (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )

    if question is None:
        raise HTTPException(
            status_code=404,
            detail="Question not found",
        )

    return question