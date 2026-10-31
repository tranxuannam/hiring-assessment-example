from sqlalchemy.exc import SQLAlchemyError

from app.services.database import check_database


def get_health_status(engine) -> tuple[str, str]:
    try:
        check_database(engine)
    except SQLAlchemyError:
        return "degraded", "unavailable"
    return "ok", "ok"
