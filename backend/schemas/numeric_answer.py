from pydantic import BaseModel, ConfigDict


class NumericAnswerCreate(BaseModel):
    correct_value: float
    tolerance: float = 0.0


class NumericAnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_id: int
    correct_value: float
    tolerance: float