from uuid import UUID

from pydantic import Field, model_validator

from app.models.assessment import AnswerType
from app.schemas.common import APIModel


class QuestionCreate(APIModel):
    role: str = Field(min_length=1, max_length=120)
    prompt: str = Field(min_length=1)
    position: int = Field(ge=1)
    evaluation_criteria: str = Field(min_length=1)
    max_score: int = Field(default=10, ge=1, le=100)


class QuestionResponse(QuestionCreate):
    id: UUID


class AnswerCreate(APIModel):
    candidate_id: UUID
    question_id: UUID
    answer_type: AnswerType = AnswerType.TEXT
    answer_text: str | None = None
    audio_path: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def validate_content(self):
        if self.answer_type == AnswerType.TEXT and not self.answer_text:
            raise ValueError("Text answers require answer_text")
        if self.answer_type == AnswerType.AUDIO and not self.audio_path:
            raise ValueError("Audio answers require audio_path")
        return self


class AnswerResponse(AnswerCreate):
    id: UUID
