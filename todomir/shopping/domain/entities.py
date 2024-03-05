from datetime import datetime
from pydantic import Field
from common.domain import entities


class ShoppingListItem(entities.DbEntity):
    name: str
    completed: datetime | None = Field(default=None)
    created: datetime
