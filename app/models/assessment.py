from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.candidate import Candidate
    from app.models.scoring import Score


class AnswerType(StrEnum):
    TEXT = "text"
    AUDIO = "audio"


class Question(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "questions"
    __table_args__ = (UniqueConstraint("role", "position", name="uq_question_role_position"),)

    role: Mapped[str] = mapped_column(String(120), index=True)
    prompt: Mapped[str] = mapped_column(Text)
    position: Mapped[int] = mapped_column(Integer)
    evaluation_criteria: Mapped[str] = mapped_column(Text)
    max_score: Mapped[int] = mapped_column(Integer, default=10)

    answers: Mapped[list["Answer"]] = relationship(back_populates="question")


class Answer(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "answers"
    __table_args__ = (
        UniqueConstraint("candidate_id", "question_id", name="uq_answer_candidate_question"),
    )

    candidate_id: Mapped[UUID] = mapped_column(ForeignKey("candidates.id"), index=True)
    question_id: Mapped[UUID] = mapped_column(ForeignKey("questions.id"), index=True)
    answer_type: Mapped[AnswerType] = mapped_column(
        Enum(AnswerType, native_enum=False, length=20), default=AnswerType.TEXT
    )
    answer_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    audio_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    candidate: Mapped["Candidate"] = relationship(back_populates="answers")
    question: Mapped["Question"] = relationship(back_populates="answers")
    score: Mapped["Score | None"] = relationship(back_populates="answer", uselist=False)
