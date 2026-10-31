from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.candidate import Candidate
from app.schemas.hr_api import (
    AssignmentCreateRequest,
    AssignmentCreateResponse,
    HRAnswerResponse,
    HRCandidateSummary,
    MockHRSignInRequest,
    MockHRSignInResponse,
    ScoreOverrideAuditResponse,
    ScoreOverrideRequest,
    ScoreOverrideResponse,
)
from app.services.authorization import require_mock_hr
from app.services.hr import (
    create_assignment,
    effective_score,
    get_answer_for_hr,
    list_candidates_by_role,
    list_score_overrides,
    override_score,
)

router = APIRouter(prefix="/hr", tags=["hr"])


@router.post("/mock-sign-in", response_model=MockHRSignInResponse)
def mock_sign_in(payload: MockHRSignInRequest, db: Session = Depends(get_db)):
    hr = require_mock_hr(db, payload.email)
    return MockHRSignInResponse(
        label=f"Mock HR sign-in: {hr.email}", header="X-Mock-HR-Email"
    )


@router.post("/assignments", response_model=AssignmentCreateResponse)
def assignment(
    payload: AssignmentCreateRequest,
    db: Session = Depends(get_db),
    hr: Candidate = Depends(require_mock_hr),
):
    try:
        item, token = create_assignment(db, payload.candidate_id, payload.role)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return AssignmentCreateResponse(
        assignment_id=item.id, personal_link_token=token, status=item.status.value
    )


@router.get("/candidates", response_model=list[HRCandidateSummary])
def candidates(
    db: Session = Depends(get_db),
    hr: Candidate = Depends(require_mock_hr),
):
    return [
        HRCandidateSummary(
            candidate_id=row.id,
            candidate_name=row.full_name,
            email=row.email,
            role=row.role.value,
            answer_count=row.answer_count,
        )
        for row in list_candidates_by_role(db)
    ]


@router.get("/answers/{answer_id}", response_model=HRAnswerResponse)
def answer(
    answer_id: UUID,
    db: Session = Depends(get_db),
    hr: Candidate = Depends(require_mock_hr),
):
    item = get_answer_for_hr(db, answer_id)
    if not item:
        raise HTTPException(status_code=404, detail="Answer not found")
    status = None
    if item.scoring_job:
        status = item.scoring_job.status.value
    return HRAnswerResponse(
        answer_id=item.id,
        candidate_id=item.candidate_id,
        candidate_name=item.candidate.full_name,
        question_id=item.question_id,
        question=item.question.prompt,
        answer_text=item.answer_text,
        audio_path=item.audio_path,
        suggested_score=float(item.score.score) if item.score else None,
        suggested_reason=item.score.reason if item.score else None,
        effective_score=effective_score(db, item),
        scoring_status=status,
    )


@router.post(
    "/answers/{answer_id}/score-override",
    response_model=ScoreOverrideResponse,
)
def score_override(
    answer_id: UUID,
    payload: ScoreOverrideRequest,
    db: Session = Depends(get_db),
    hr: Candidate = Depends(require_mock_hr),
):
    try:
        audit = override_score(db, hr, answer_id, payload.score, payload.reason)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ScoreOverrideResponse(
        answer_id=answer_id, score=int(audit.new_score), reason=audit.reason
    )


@router.get(
    "/answers/{answer_id}/score-overrides",
    response_model=list[ScoreOverrideAuditResponse],
)
def score_overrides(
    answer_id: UUID,
    db: Session = Depends(get_db),
    hr: Candidate = Depends(require_mock_hr),
):
    try:
        audits = list_score_overrides(db, answer_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return [
        ScoreOverrideAuditResponse(
            previous_score=float(item.previous_score),
            new_score=float(item.new_score),
            reason=item.reason,
            hr_user_id=item.hr_user_id,
        )
        for item in audits
    ]
