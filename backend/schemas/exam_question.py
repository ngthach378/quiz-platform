from pydantic import BaseModel, ConfigDict


class ExamQuestionCreate(BaseModel):
    question_id: int
    part: int
    question_number: int


class ExamQuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    exam_id: int
    question_id: int
    part: int
    question_number: int