from ninja import NinjaAPI
from todos.domain import entities, repositories
from todos.api import schemas


api = NinjaAPI()


@api.post("/tasks")
def create_task(request, task: schemas.TodoTaskSchema):
    repository = repositories.TodoTaskRepository()
    entity = entities.TodoTask(name=task.name, external_id=task.external_id)
    repository.persist(entity)
    return entity
