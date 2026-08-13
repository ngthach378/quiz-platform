from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.attempt import Attempt
from backend.models.attempt_answer import AttemptAnswer
from backend.models.attempt_statement_answer import AttemptStatementAnswer
from backend.models.exam_question import ExamQuestion
from backend.models.question import Question
from backend.models.question_option import QuestionOption
from backend.models.question_statement import QuestionStatement
from backend.schemas.attempt_answer import (
    AttemptAnswerCreate,
    AttemptAnswerResponse,
)
from backend.schemas.attempt_statement_answer import (
    AttemptStatementAnswerCreate,
    AttemptStatementAnswerResponse,
)


router = APIRouter(
    prefix="/attempts",
    tags=["Attempt Answers"],
)


@router.post(
    "/{attempt_id}/answers",
    response_model=AttemptAnswerResponse,
)
def create_attempt_answer(
    attempt_id: int,
    data: AttemptAnswerCreate,
    db: Session = Depends(get_db),
):
    # 1. Kiểm tra attempt
    attempt = (
        db.query(Attempt)
        .filter(Attempt.id == attempt_id)
        .first()
    )

    if attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Attempt not found",
        )

    if attempt.status != "IN_PROGRESS":
        raise HTTPException(
            status_code=400,
            detail="Attempt is not in progress",
        )

    # 2. Kiểm tra question có thuộc exam của attempt không
    exam_question = (
        db.query(ExamQuestion)
        .filter(
            ExamQuestion.exam_id == attempt.exam_id,
            ExamQuestion.question_id == data.question_id,
        )
        .first()
    )

    if exam_question is None:
        raise HTTPException(
            status_code=400,
            detail="Question does not belong to this exam",
        )

    question = (
        db.query(Question)
        .filter(Question.id == data.question_id)
        .first()
    )

    if question is None:
        raise HTTPException(
            status_code=404,
            detail="Question not found",
        )

    # 3. Không cho trả lời cùng một question 2 lần
    existing_answer = (
        db.query(AttemptAnswer)
        .filter(
            AttemptAnswer.attempt_id == attempt_id,
            AttemptAnswer.question_id == data.question_id,
        )
        .first()
    )

    if existing_answer:
        raise HTTPException(
            status_code=400,
            detail="Question has already been answered",
        )

    # 4. Kiểm tra kiểu câu hỏi
    if question.question_type == "MCQ":
        if data.selected_option_id is None:
            raise HTTPException(
                status_code=400,
                detail="MCQ requires selected_option_id",
            )

        if data.numeric_answer is not None:
            raise HTTPException(
                status_code=400,
                detail="MCQ cannot have numeric_answer",
            )

        option = (
            db.query(QuestionOption)
            .filter(
                QuestionOption.id == data.selected_option_id,
                QuestionOption.question_id == data.question_id,
            )
            .first()
        )

        if option is None:
            raise HTTPException(
                status_code=400,
                detail="Selected option does not belong to this question",
            )

    elif question.question_type == "NUMERIC":
        if data.numeric_answer is None:
            raise HTTPException(
                status_code=400,
                detail="NUMERIC requires numeric_answer",
            )

        if data.selected_option_id is not None:
            raise HTTPException(
                status_code=400,
                detail="NUMERIC cannot have selected_option_id",
            )

    elif question.question_type == "TRUE_FALSE":
        if (
            data.selected_option_id is not None
            or data.numeric_answer is not None
        ):
            raise HTTPException(
                status_code=400,
                detail="TRUE_FALSE answers must use statement answers",
            )

    answer = AttemptAnswer(
        attempt_id=attempt_id,
        question_id=data.question_id,
        selected_option_id=data.selected_option_id,
        numeric_answer=data.numeric_answer,
        is_correct=None,
    )

    db.add(answer)
    db.commit()
    db.refresh(answer)

    return answer


@router.post(
    "/{attempt_id}/answers/{attempt_answer_id}/statements",
    response_model=AttemptStatementAnswerResponse,
)
def create_attempt_statement_answer(
    attempt_id: int,
    attempt_answer_id: int,
    data: AttemptStatementAnswerCreate,
    db: Session = Depends(get_db),
):
    # 1. Kiểm tra attempt
    attempt = (
        db.query(Attempt)
        .filter(Attempt.id == attempt_id)
        .first()
    )

    if attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Attempt not found",
        )

    if attempt.status != "IN_PROGRESS":
        raise HTTPException(
            status_code=400,
            detail="Attempt is not in progress",
        )

    # 2. Kiểm tra attempt answer
    attempt_answer = (
        db.query(AttemptAnswer)
        .filter(
            AttemptAnswer.id == attempt_answer_id,
            AttemptAnswer.attempt_id == attempt_id,
        )
        .first()
    )

    if attempt_answer is None:
        raise HTTPException(
            status_code=404,
            detail="Attempt answer not found",
        )

    # 3. Chỉ TRUE_FALSE mới dùng statement answers
    question = (
        db.query(Question)
        .filter(Question.id == attempt_answer.question_id)
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
            detail="Statement answers can only be used for TRUE_FALSE questions",
        )

    # 4. Kiểm tra statement
    statement = (
        db.query(QuestionStatement)
        .filter(
            QuestionStatement.id == data.statement_id,
            QuestionStatement.question_id == attempt_answer.question_id,
        )
        .first()
    )

    if statement is None:
        raise HTTPException(
            status_code=400,
            detail="Statement does not belong to this question",
        )

    # 5. Không cho trả lời statement hai lần
    existing_answer = (
        db.query(AttemptStatementAnswer)
        .filter(
            AttemptStatementAnswer.attempt_answer_id == attempt_answer_id,
            AttemptStatementAnswer.statement_id == data.statement_id,
        )
        .first()
    )

    if existing_answer:
        raise HTTPException(
            status_code=400,
            detail="Statement has already been answered",
        )

    statement_answer = AttemptStatementAnswer(
        attempt_answer_id=attempt_answer_id,
        statement_id=data.statement_id,
        selected_answer=data.selected_answer,
    )

    db.add(statement_answer)
    db.commit()
    db.refresh(statement_answer)

    return statement_answer