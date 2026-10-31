from pydantic import BaseModel, ConfigDict


class APIModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    status: str
    database: str
