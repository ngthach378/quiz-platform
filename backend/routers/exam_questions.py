from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.exam import Exam
from backend.models.exam_question import ExamQuestion
from backend.models.question import Question
from backend.schemas.exam_question import (
    ExamQuestionCreate,
    ExamQuestionResponse,
)


router = APIRouter(
    prefix="/exams",
    tags=["Exam Questions"],
)


@router.post(
    "/{exam_id}/questions",
    response_model=ExamQuestionResponse,
)
def add_question_to_exam(
    exam_id: int,
    data: ExamQuestionCreate,
    db: Session = Depends(get_db),
):
    # 1. Kiểm tra exam
    exam = (
        db.query(Exam)
        .filter(Exam.id == exam_id)
        .first()
    )

    if exam is None:
        raise HTTPException(
            status_code=404,
            detail="Exam not found",
        )

    # 2. Kiểm tra question
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

    # 3. Kiểm tra part
    if data.part not in {1, 2, 3}:
        raise HTTPException(
            status_code=400,
            detail="Part must be 1, 2, or 3",
        )

    # 4. Kiểm tra question_type tương ứng với part
    expected_type = {
        1: "MCQ",
        2: "TRUE_FALSE",
        3: "NUMERIC",
    }[data.part]

    if question.question_type != expected_type:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Part {data.part} requires "
                f"{expected_type} questions"
            ),
        )

    # 5. Kiểm tra question number theo cấu trúc đề
    valid_ranges = {
        1: range(1, 13),    # 1-12
        2: range(13, 17),   # 13-16
        3: range(17, 23),   # 17-22
    }

    if data.question_number not in valid_ranges[data.part]:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Question number is invalid for part {data.part}"
            ),
        )

    # 6. Không cho cùng một question xuất hiện 2 lần
    existing_question = (
        db.query(ExamQuestion)
        .filter(
            ExamQuestion.exam_id == exam_id,
            ExamQuestion.question_id == data.question_id,
        )
        .first()
    )

    if existing_question:
        raise HTTPException(
            status_code=400,
            detail="Question is already in this exam",
        )

    # 7. Không cho trùng question number trong cùng exam
    existing_number = (
        db.query(ExamQuestion)
        .filter(
            ExamQuestion.exam_id == exam_id,
            ExamQuestion.question_number == data.question_number,
        )
        .first()
    )

    if existing_number:
        raise HTTPException(
            status_code=400,
            detail="Question number already exists in this exam",
        )

    exam_question = ExamQuestion(
        exam_id=exam_id,
        question_id=data.question_id,
        part=data.part,
        question_number=data.question_number,
    )

    db.add(exam_question)
    db.commit()
    db.refresh(exam_question)

    return exam_question


@router.get(
    "/{exam_id}/questions",
    response_model=list[ExamQuestionResponse],
)
def get_exam_questions(
    exam_id: int,
    db: Session = Depends(get_db),
):
    exam = (
        db.query(Exam)
        .filter(Exam.id == exam_id)
        .first()
    )

    if exam is None:
        raise HTTPException(
            status_code=404,
            detail="Exam not found",
        )

    return (
        db.query(ExamQuestion)
        .filter(ExamQuestion.exam_id == exam_id)
        .order_by(ExamQuestion.question_number)
        .all()
    )