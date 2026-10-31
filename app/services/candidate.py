from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Answer, AssessmentAssignment, Question
from app.models.assessment import AnswerType, AssignmentStatus
from app.services.authorization import get_assignment_by_token
from app.services.scoring import enqueue_scoring_job


def get_next_question(db: Session, token: str):
    assignment = get_assignment_by_token(db, token)
    if assignment.status != AssignmentStatus.ACTIVE:
        return assignment, None
    answered = select(Answer.question_id).where(
        Answer.candidate_id == assignment.candidate_id
    )
    question = db.scalar(
        select(Question)
        .where(Question.role == assignment.role, Question.id.not_in(answered))
        .order_by(Question.position)
    )
    return assignment, question


def save_text_answer(db: Session, token: str, question_id, answer_text: str) -> Answer:
    assignment = get_assignment_by_token(db, token)
    if assignment.status != AssignmentStatus.ACTIVE:
        raise ValueError("Assignment is no longer accepting answers")
    question = db.scalar(
        select(Question).where(
            Question.id == question_id, Question.role == assignment.role
        )
    )
    if not question:
        raise LookupError("Question not found")
    existing = db.scalar(
        select(Answer).where(
            Answer.candidate_id == assignment.candidate_id,
            Answer.question_id == question_id,
        )
    )
    if existing:
        return existing
    answer = Answer(
        candidate_id=assignment.candidate_id,
        question_id=question_id,
        answer_type=AnswerType.TEXT,
        answer_text=answer_text,
    )
    db.add(answer)
    db.flush()
    enqueue_scoring_job(db, answer.id)
    db.commit()
    db.refresh(answer)
    return answer


def submit_assignment(db: Session, token: str) -> AssessmentAssignment:
    assignment = get_assignment_by_token(db, token)
    if assignment.status == AssignmentStatus.ACTIVE:
        assignment.status = AssignmentStatus.SUBMITTED
        db.commit()
        db.refresh(assignment)
    return assignment
