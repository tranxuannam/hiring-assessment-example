from uuid import UUID

from pydantic import EmailStr, Field

from app.models.candidate import Role
from app.schemas.common import APIModel


class CandidateCreate(APIModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=200)
    role: Role = Role.CANDIDATE


class CandidateResponse(APIModel):
    id: UUID
    email: EmailStr
    full_name: str
    role: Role
    is_active: bool
