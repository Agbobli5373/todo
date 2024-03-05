from datetime import date

from asgiref.sync import async_to_sync
from todomir.celery import app

from todos.domain import entities, repositories


@app.task
def create_tasks_for_today():
    task_repository = repositories.TodoTaskRepository()
    schedule_repository = repositories.TodoTaskScheduleRepository()

    get_unfinished_tasks = async_to_sync(task_repository.get_unfinished)
    unfinished_tasks = get_unfinished_tasks()

    today = date.today()

    get_scheduled_for_day = async_to_sync(schedule_repository.get_scheduled_for_day)
    scheduled_tasks = get_scheduled_for_day(
        today,
        exclude_ids=[task.schedule_id for task in unfinished_tasks if task.schedule_id],
    )

    todo_tasks = [
        entities.TodoTask(
            name=scheduled_task.name,
            schedule_id=scheduled_task.id,
        )
        for scheduled_task in scheduled_tasks
    ]

    bulk_create = async_to_sync(task_repository.bulk_create)
    bulk_create(todo_tasks)


@app.task
def clean_finished_tasks_and_schedules():
    task_repository = repositories.TodoTaskRepository()
    schedule_repository = repositories.TodoTaskScheduleRepository()

    remove_all_tasks = async_to_sync(task_repository.remove_all_finished)
    remove_all_schedules = async_to_sync(schedule_repository.remove_all_finished)

    remove_all_tasks()
    remove_all_schedules()
