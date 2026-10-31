import hashlib
import secrets

from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import AssessmentAssignment, Candidate
from app.models.candidate import Role


def create_personal_token() -> tuple[str, str]:
    token = secrets.token_urlsafe(32)
    return token, hashlib.sha256(token.encode()).hexdigest()


def get_assignment_by_token(db: Session, token: str) -> AssessmentAssignment:
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    assignment = db.scalar(
        select(AssessmentAssignment).where(AssessmentAssignment.token_hash == token_hash)
    )
    if not assignment or assignment.status.value == "closed":
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


def require_mock_hr(
    db: Session = Depends(get_db),
    x_mock_hr_email: str | None = Header(default=None),
) -> Candidate:
    if not x_mock_hr_email:
        raise HTTPException(status_code=401, detail="Mock HR sign-in required")
    hr = db.scalar(
        select(Candidate).where(
            Candidate.email == x_mock_hr_email,
            Candidate.role == Role.HR,
            Candidate.is_active.is_(True),
        )
    )
    if not hr:
        raise HTTPException(status_code=403, detail="HR authorization required")
    return hr
