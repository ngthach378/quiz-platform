from pydantic import BaseModel, ConfigDict


class AttemptAnswerCreate(BaseModel):
    question_id: int
    selected_option_id: int | None = None
    numeric_answer: str | None = None


class AttemptAnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    attempt_id: int
    question_id: int
    selected_option_id: int | None
    numeric_answer: str | None
    is_correct: bool | None