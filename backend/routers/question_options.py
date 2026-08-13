from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.question import Question
from backend.models.question_option import QuestionOption
from backend.schemas.question_option import (
    QuestionOptionCreate,
    QuestionOptionResponse,
)

router = APIRouter(
    prefix="/questions",
    tags=["Question Options"],
)


@router.post(
    "/{question_id}/options",
    response_model=QuestionOptionResponse,
)
def create_option(
    question_id: int,
    option_data: QuestionOptionCreate,
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

    if question.question_type != "MCQ":
        raise HTTPException(
            status_code=400,
            detail="Options can only be added to MCQ questions",
        )

    if option_data.option_label not in {"A", "B", "C", "D"}:
        raise HTTPException(
            status_code=400,
            detail="Option label must be A, B, C, or D",
        )

    if option_data.position not in {1, 2, 3, 4}:
        raise HTTPException(
            status_code=400,
            detail="Option position must be between 1 and 4",
        )

    existing_option = (
        db.query(QuestionOption)
        .filter(
            QuestionOption.question_id == question_id,
            (
                (QuestionOption.option_label == option_data.option_label)
                | (QuestionOption.position == option_data.position)
            ),
        )
        .first()
    )

    if existing_option:
        raise HTTPException(
            status_code=400,
            detail="Option label or position already exists",
        )

    option_count = (
        db.query(QuestionOption)
        .filter(QuestionOption.question_id == question_id)
        .count()
    )

    if option_count >= 4:
        raise HTTPException(
            status_code=400,
            detail="A MCQ question can have at most 4 options",
        )

    if option_data.is_correct:
        correct_count = (
            db.query(QuestionOption)
            .filter(
                QuestionOption.question_id == question_id,
                QuestionOption.is_correct.is_(True),
            )
            .count()
        )

        if correct_count >= 1:
            raise HTTPException(
                status_code=400,
                detail="A MCQ question can have only one correct option",
            )

    option = QuestionOption(
        question_id=question_id,
        option_label=option_data.option_label,
        content=option_data.content,
        position=option_data.position,
        is_correct=option_data.is_correct,
    )

    db.add(option)
    db.commit()
    db.refresh(option)

    return option


@router.get(
    "/{question_id}/options",
    response_model=list[QuestionOptionResponse],
)
def get_options(
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

    return (
        db.query(QuestionOption)
        .filter(QuestionOption.question_id == question_id)
        .order_by(QuestionOption.position)
        .all()
    )