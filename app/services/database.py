from sqlalchemy import text
from sqlalchemy.engine import Engine

from app.db.base import Base
from app.models import Answer, Candidate, Question, Score, ScoringJob


def initialize_database(engine: Engine) -> None:
    Base.metadata.create_all(bind=engine)


def check_database(engine: Engine) -> bool:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return True
