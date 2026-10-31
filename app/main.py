import logging

from fastapi import FastAPI

from app.api.health import router as health_router
from app.config import get_settings
from app.db.base import Base
from app.db.session import engine
from app.services.database import initialize_database

settings = get_settings()
logging.basicConfig(level=settings.log_level)

app = FastAPI(title=settings.app_name)
app.include_router(health_router)


@app.on_event("startup")
def startup() -> None:
    initialize_database(engine)
