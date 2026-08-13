from datetime import datetime

from pydantic import BaseModel, ConfigDict

from backend.models.question import QuestionType


class QuestionCreate(BaseModel):
    content: str
    question_type: QuestionType
    explanation: str | None = None
    difficulty: str | None = None


class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    question_type: QuestionType
    explanation: str | None
    difficulty: str | None
    created_at: datetime
    updated_at: datetime