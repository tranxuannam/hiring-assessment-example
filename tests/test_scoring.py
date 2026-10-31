from uuid import uuid4

from sqlalchemy.orm import Session

from app.config import Settings
from app.models import Answer, Candidate, Question, Score, ScoringJob
from app.models.scoring import ScoringJobStatus
from app.schemas.scoring_result import ScoringResult
from app.services.scoring import enqueue_scoring_job, process_scoring_job


class FakeLLM:
    model_name = "fake-test-model"

    def __init__(self, result=None, error=None):
        self.result = result or ScoringResult(score=3, reason="Mostly correct.")
        self.error = error
        self.calls = 0

    def score(self, **kwargs):
        self.calls += 1
        if self.error:
            raise self.error
        return self.result


def make_answer(session):
    candidate = Candidate(email=f"{uuid4()}@example.com", full_name="Candidate")
    question = Question(
        role="Backend Engineer",
        prompt="Explain a transaction.",
        position=1,
        evaluation_criteria="Look for atomicity and rollback.",
    )
    session.add_all([candidate, question])
    session.commit()
    answer = Answer(
        candidate_id=candidate.id,
        question_id=question.id,
        answer_text="A transaction is an atomic unit of work.",
    )
    session.add(answer)
    session.commit()
    return answer


def test_scoring_persists_structured_result_and_is_idempotent(test_engine):
    with Session(test_engine) as session:
        answer = make_answer(session)
        job = enqueue_scoring_job(session, answer.id)
        client = FakeLLM()

        assert process_scoring_job(session, job.id, client).status == ScoringJobStatus.SCORED
        process_scoring_job(session, job.id, client)

        assert client.calls == 1
        assert session.query(Score).filter_by(answer_id=answer.id).count() == 1


def test_scoring_retries_then_fails(test_engine):
    with Session(test_engine) as session:
        answer = make_answer(session)
        job = enqueue_scoring_job(session, answer.id)
        client = FakeLLM(error=RuntimeError("provider unavailable"))
        settings = Settings(scoring_max_attempts=2)

        first = process_scoring_job(session, job.id, client, settings)
        assert first.status == ScoringJobStatus.QUEUED
        second = process_scoring_job(session, job.id, client, settings)
        assert second.status == ScoringJobStatus.FAILED
        assert second.attempts == 2


def test_invalid_output_can_be_sent_to_human_review(test_engine):
    from app.services.llm import InvalidLLMOutput

    with Session(test_engine) as session:
        answer = make_answer(session)
        job = enqueue_scoring_job(session, answer.id)
        result = process_scoring_job(
            session, job.id, FakeLLM(error=InvalidLLMOutput("invalid JSON"))
        )
        assert result.status == ScoringJobStatus.NEEDS_HUMAN
