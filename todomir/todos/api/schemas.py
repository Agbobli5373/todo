from ninja import Schema
from pydantic.functional_validators import AfterValidator
from typing import Annotated

from todos.api import validators

ExternalID = Annotated[str, AfterValidator(validators.validate_external_id)]


class TodoTaskSchema(Schema):
    name: str
    external_id: ExternalID | None = None
