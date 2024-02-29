from todos.domain import repositories


def validate_external_id(external_id: str | None):
    if not external_id:
        return None

    repository = repositories.TodoTaskRepository()
    assert (
        repository.get_by_external_id(external_id) is None
    ), f"Task with {external_id=} exists"
    return external_id
