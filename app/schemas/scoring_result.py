from pydantic import BaseModel, ConfigDict, Field


class ScoringResult(BaseModel):
    """The only model output accepted by the scoring service."""

    model_config = ConfigDict(extra="forbid", strict=True)

    score: int = Field(ge=1, le=4)
    reason: str = Field(min_length=1, max_length=4000)
