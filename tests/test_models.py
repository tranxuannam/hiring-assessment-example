from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Answer, Candidate, Question


def test_answer_is_unique_per_candidate_and_question(test_engine):
    with Session(test_engine) as session:
        candidate = Candidate(email="candidate@example.com", full_name="Candidate")
        question = Question(
            role="Backend Engineer",
            prompt="Explain a transaction.",
            position=1,
            evaluation_criteria="Correctness",
        )
        session.add_all([candidate, question])
        session.commit()

        session.add(
            Answer(
                candidate_id=candidate.id,
                question_id=question.id,
                answer_text="Use an atomic unit of work.",
            )
        )
        session.commit()
        session.add(
            Answer(
                candidate_id=candidate.id,
                question_id=question.id,
                answer_text="A duplicate answer.",
            )
        )

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
        else:
            raise AssertionError("duplicate answer was accepted")


def test_score_and_job_are_one_per_answer(test_engine):
    from app.models import Score, ScoringJob

    with Session(test_engine) as session:
        candidate = Candidate(email="candidate2@example.com", full_name="Candidate Two")
        question = Question(
            role="Backend Engineer",
            prompt="Explain a queue.",
            position=2,
            evaluation_criteria="Reliability",
        )
        session.add_all([candidate, question])
        session.commit()
        answer = Answer(
            candidate_id=candidate.id,
            question_id=question.id,
            answer_text="A durable work list.",
        )
        session.add(answer)
        session.commit()
        session.add(ScoringJob(answer_id=answer.id))
        session.commit()
        session.add(ScoringJob(answer_id=answer.id))
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
        else:
            raise AssertionError("duplicate scoring job was accepted")

        session.add(
            Score(
                answer_id=answer.id,
                score=8,
                reason="Clear answer.",
                model_name="test-model",
                prompt_version="v1",
            )
        )
        session.commit()
        session.add(
            Score(
                answer_id=answer.id,
                score=7,
                reason="Duplicate score.",
                model_name="test-model",
                prompt_version="v1",
            )
        )
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
        else:
            raise AssertionError("duplicate score was accepted")
