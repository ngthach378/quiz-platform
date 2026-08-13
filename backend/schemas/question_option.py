from pydantic import BaseModel, ConfigDict


class QuestionOptionCreate(BaseModel):
    option_label: str
    content: str
    position: int
    is_correct: bool


class QuestionOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_id: int
    option_label: str
    content: str
    position: int
    is_correct: bool