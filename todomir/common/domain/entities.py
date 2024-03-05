from pydantic import BaseModel, Field


class DbEntity(BaseModel):
    id: int | None = Field(default=None)
