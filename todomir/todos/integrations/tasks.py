from datetime import date
from todomir.celery import app

from todos.domain import entities, repositories
from todos.integrations import wastes


def _check_schedule_and_create_task(schedule: dict, task_name: str):
    today = date.today()
    year, month, day = today.year, today.month, today.day

    if pickup_dates := schedule.get(year, {}).get(month):
        # subtract one day to create task day before pickup
        if day in [d - 1 for d in pickup_dates]:
            task = entities.TodoTask(name=task_name)
            repositories.TodoTaskRepository().persist(task)


@app.task
def create_task_to_prepare_wastes():
    _check_schedule_and_create_task(
        schedule=wastes.SCHEDULE_MIXED_WASTES,
        task_name="Wystawić kubeł na śmieci mieszane",
    )
    _check_schedule_and_create_task(
        schedule=wastes.SCHEDULE_SEGREGATED_WASTES,
        task_name="Wystawić śmieci segregowane",
    )
