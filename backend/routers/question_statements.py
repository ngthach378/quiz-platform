from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.question import Question
from backend.models.question_statement import QuestionStatement
from backend.schemas.question_statement import (
    QuestionStatementCreate,
    QuestionStatementResponse,
)


router = APIRouter(
    prefix="/questions",
    tags=["Question Statements"],
)


@router.post(
    "/{question_id}/statements",
    response_model=QuestionStatementResponse,
)
def create_statement(
    question_id: int,
    statement_data: QuestionStatementCreate,
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

    if question.question_type != "TRUE_FALSE":
        raise HTTPException(
            status_code=400,
            detail="Statements can only be added to TRUE_FALSE questions",
        )

    if statement_data.position not in {1, 2, 3, 4}:
        raise HTTPException(
            status_code=400,
            detail="Statement position must be between 1 and 4",
        )

    existing_statement = (
        db.query(QuestionStatement)
        .filter(
            QuestionStatement.question_id == question_id,
            QuestionStatement.position == statement_data.position,
        )
        .first()
    )

    if existing_statement:
        raise HTTPException(
            status_code=400,
            detail="Statement position already exists",
        )

    statement_count = (
        db.query(QuestionStatement)
        .filter(QuestionStatement.question_id == question_id)
        .count()
    )

    if statement_count >= 4:
        raise HTTPException(
            status_code=400,
            detail="A TRUE_FALSE question can have at most 4 statements",
        )

    statement = QuestionStatement(
        question_id=question_id,
        content=statement_data.content,
        position=statement_data.position,
        correct_answer=statement_data.correct_answer,
    )

    db.add(statement)
    db.commit()
    db.refresh(statement)

    return statement


@router.get(
    "/{question_id}/statements",
    response_model=list[QuestionStatementResponse],
)
def get_statements(
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
        db.query(QuestionStatement)
        .filter(QuestionStatement.question_id == question_id)
        .order_by(QuestionStatement.position)
        .all()
    )
