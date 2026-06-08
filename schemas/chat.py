from pydantic import BaseModel, field_validator


class QuestionRequest(BaseModel):
    question: str
    k: int = 5

    @field_validator("question")
    @classmethod
    def question_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Question must not be empty")
        return v
