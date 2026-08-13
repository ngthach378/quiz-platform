from pydantic import BaseModel, ConfigDict


class AttemptStatementAnswerCreate(BaseModel):
    statement_id: int
    selected_answer: bool


class AttemptStatementAnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    attempt_answer_id: int
    statement_id: int
    selected_answer: bool