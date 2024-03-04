from datetime import datetime
from pydantic import BaseModel, Field


class ShoppingListItem(BaseModel):
    id: int | None = Field(default=None)
    name: str
    completed: datetime | None = Field(default=None)
    created: datetime
