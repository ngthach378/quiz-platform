from pydantic import BaseModel, ConfigDict


class QuestionStatementCreate(BaseModel):
    content: str
    position: int
    correct_answer: bool


class QuestionStatementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_id: int
    content: str
    position: int
    correct_answer: bool