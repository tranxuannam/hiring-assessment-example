from uuid import UUID

from pydantic import Field

from app.models.scoring import ScoringJobStatus
from app.schemas.common import APIModel


class ScoringJobResponse(APIModel):
    id: UUID
    answer_id: UUID
    status: ScoringJobStatus
    attempts: int
    last_error: str | None


class ScoreResponse(APIModel):
    id: UUID
    answer_id: UUID
    score: float = Field(ge=0)
    reason: str
    model_name: str
    prompt_version: str
