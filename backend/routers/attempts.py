from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.attempt import Attempt
from backend.models.exam import Exam
from backend.models.user import User
from backend.schemas.attempt import AttemptCreate, AttemptResponse


router = APIRouter(
    prefix="/attempts",
    tags=["Attempts"],
)


@router.post("/", response_model=AttemptResponse)
def create_attempt(
    data: AttemptCreate,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.id == data.user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    exam = (
        db.query(Exam)
        .filter(Exam.id == data.exam_id)
        .first()
    )

    if exam is None:
        raise HTTPException(
            status_code=404,
            detail="Exam not found",
        )

    attempt = Attempt(
        user_id=data.user_id,
        exam_id=data.exam_id,
        started_at=datetime.now(timezone.utc),
        submitted_at=None,
        score=None,
        status="IN_PROGRESS",
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt


@router.get("/{attempt_id}", response_model=AttemptResponse)
def get_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
):
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

    return attempt