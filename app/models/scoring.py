from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.assessment import Answer


class ScoringJobStatus(StrEnum):
    QUEUED = "queued"
    PROCESSING = "processing"
    SCORED = "scored"
    FAILED = "failed"
    NEEDS_HUMAN = "needs_human"


class ScoringJob(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "scoring_jobs"

    answer_id: Mapped[UUID] = mapped_column(
        ForeignKey("answers.id"), unique=True, index=True
    )
    status: Mapped[ScoringJobStatus] = mapped_column(
        Enum(ScoringJobStatus, native_enum=False, length=20),
        default=ScoringJobStatus.QUEUED,
        nullable=False,
    )
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    available_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    answer: Mapped["Answer"] = relationship()


class Score(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "scores"
    __table_args__ = (UniqueConstraint("answer_id", name="uq_score_answer"),)

    answer_id: Mapped[UUID] = mapped_column(ForeignKey("answers.id"), index=True)
    score: Mapped[float] = mapped_column(Numeric(5, 2))
    reason: Mapped[str] = mapped_column(Text)
    model_name: Mapped[str] = mapped_column(String(120))
    prompt_version: Mapped[str] = mapped_column(String(80))

    answer: Mapped["Answer"] = relationship(back_populates="score")
