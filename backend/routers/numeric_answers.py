from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.question import Question
from backend.models.numeric_answer import NumericAnswer
from backend.schemas.numeric_answer import (
    NumericAnswerCreate,
    NumericAnswerResponse,
)


router = APIRouter(
    prefix="/questions",
    tags=["Numeric Answers"],
)


@router.post(
    "/{question_id}/numeric-answer",
    response_model=NumericAnswerResponse,
)
def create_numeric_answer(
    question_id: int,
    answer_data: NumericAnswerCreate,
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

    if question.question_type != "NUMERIC":
        raise HTTPException(
            status_code=400,
            detail="Numeric answer can only be added to NUMERIC questions",
        )

    if answer_data.tolerance < 0:
        raise HTTPException(
            status_code=400,
            detail="Tolerance cannot be negative",
        )

    existing_answer = (
        db.query(NumericAnswer)
        .filter(NumericAnswer.question_id == question_id)
        .first()
    )

    if existing_answer:
        raise HTTPException(
            status_code=400,
            detail="Numeric answer already exists",
        )

    answer = NumericAnswer(
        question_id=question_id,
        correct_value=answer_data.correct_value,
        tolerance=answer_data.tolerance,
    )

    db.add(answer)
    db.commit()
    db.refresh(answer)

    return answer


@router.get(
    "/{question_id}/numeric-answer",
    response_model=NumericAnswerResponse,
)
def get_numeric_answer(
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

    answer = (
        db.query(NumericAnswer)
        .filter(NumericAnswer.question_id == question_id)
        .first()
    )

    if answer is None:
        raise HTTPException(
            status_code=404,
            detail="Numeric answer not found",
        )

    return answer