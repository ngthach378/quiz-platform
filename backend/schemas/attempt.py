from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AttemptCreate(BaseModel):
    user_id: int
    exam_id: int


class AttemptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    exam_id: int
    started_at: datetime
    submitted_at: datetime | None
    score: float | None
    status: str