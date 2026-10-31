import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.main import app
from app.api.health import get_engine


@pytest.fixture
def test_engine():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(test_engine):
    app.dependency_overrides[get_engine] = lambda: test_engine
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
