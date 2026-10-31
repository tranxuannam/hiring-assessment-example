from fastapi import APIRouter, Depends
from sqlalchemy.engine import Engine

from app.db.session import engine as default_engine
from app.schemas.common import HealthResponse
from app.services.health import get_health_status

router = APIRouter(tags=["health"])


def get_engine() -> Engine:
    return default_engine


@router.get("/health", response_model=HealthResponse)
def health(engine: Engine = Depends(get_engine)) -> HealthResponse:
    status, database = get_health_status(engine)
    return HealthResponse(status=status, database=database)
