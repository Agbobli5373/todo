from datetime import datetime, timedelta

from django.core.exceptions import ValidationError

from todos.domain import entities, repositories


def get_tasks() -> list[entities.TodoTask]:
    repository = repositories.TodoTaskRepository()
    return repository.get_list()


def complete_task(task_id: int):
    task_repository = repositories.TodoTaskRepository()
    task = task_repository.get_by_id(task_id)

    if not task:
        raise ValidationError("Task does not exist")

    task.completed_at = datetime.now()
    task_repository.persist(task)

    schedule_repository = repositories.TodoTaskScheduleRepository()
    if task.schedule_id and (
        schedule := schedule_repository.get_by_id(task.schedule_id)
    ):
        if schedule.repeat_every_x_days:
            schedule.day_planned_to_complete = (
                schedule.day_planned_to_complete
                + timedelta(days=schedule.repeat_every_x_days)
            )
            schedule_repository.persist(schedule)
        elif schedule.repeat_every_x_weeks:
            schedule.day_planned_to_complete = (
                schedule.day_planned_to_complete
                + timedelta(weeks=schedule.repeat_every_x_weeks)
            )
            schedule_repository.persist(schedule)
        elif schedule.repeat_every_x_months:
            schedule.day_planned_to_complete = (
                schedule.day_planned_to_complete
                + timedelta(weeks=schedule.repeat_every_x_months * 4)
            )
            schedule_repository.persist(schedule)
        else:
            schedule_repository.remove(schedule)


def add_new_task(new_task: str):
    task_repository = repositories.TodoTaskRepository()
    task = entities.TodoTask(name=new_task)
    task_repository.persist(task)
