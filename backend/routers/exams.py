from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.exam import Exam

router = APIRouter(
    prefix="/exams",
    tags=["Exams"],
)


@router.post("/")
def create_exam(
    title: str,
    year: int,
    subject: str,
    description: str | None = None,
    db: Session = Depends(get_db),
):
    exam = Exam(
        title=title,
        year=year,
        subject=subject,
        description=description,
        is_published=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(exam)
    db.commit()
    db.refresh(exam)

    return exam


@router.get("/")
def get_exams(
    db: Session = Depends(get_db),
):
    return db.query(Exam).all()


@router.get("/{exam_id}")
def get_exam(
    exam_id: int,
    db: Session = Depends(get_db),
):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()

    if exam is None:
        raise HTTPException(
            status_code=404,
            detail="Exam not found",
        )

    return exam