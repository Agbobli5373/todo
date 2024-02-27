from datetime import date
from todomir.celery import app

from todos.domain import entities, repositories


@app.task
def create_tasks_for_today():
    task_repository = repositories.TodoTaskRepository()
    schedule_repository = repositories.TodoTaskScheduleRepository()

    unfinished_tasks = task_repository.get_unfinished()
    today = date.today()
    scheduled_tasks = schedule_repository.get_scheduled_for_day(
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

    task_repository.persist_all(todo_tasks)


@app.task
def clean_finished_tasks_and_schedules():
    task_repository = repositories.TodoTaskRepository()
    schedule_repository = repositories.TodoTaskScheduleRepository()

    task_repository.remove_all_finished()
    schedule_repository.remove_all_finished()
