from datetime import datetime, timedelta, date

from django.core.exceptions import ValidationError

from todos.domain import entities, repositories


async def get_tasks() -> list[entities.TodoTask]:
    repository = repositories.TodoTaskRepository()
    return await repository.get_list()


async def complete_task(task_id: int):
    task_repository = repositories.TodoTaskRepository()
    task = await task_repository.get_by_id(task_id)

    if not task:
        raise ValidationError("Task does not exist")

    task.completed_at = datetime.now()
    await task_repository.persist(task)

    schedule_repository = repositories.TodoTaskScheduleRepository()
    if task.schedule_id and (
        schedule := await schedule_repository.get_by_id(task.schedule_id)
    ):
        if schedule.repeat_every_x_days:
            schedule.day_planned_to_complete = date.today() + timedelta(
                days=schedule.repeat_every_x_days
            )
            await schedule_repository.persist(schedule)
        elif schedule.repeat_every_x_weeks:
            schedule.day_planned_to_complete = (
                schedule.day_planned_to_complete
                + timedelta(weeks=schedule.repeat_every_x_weeks)
            )
            if schedule.day_planned_to_complete <= date.today():
                schedule.day_planned_to_complete = date.today() + timedelta(
                    weeks=schedule.repeat_every_x_weeks
                )
            await schedule_repository.persist(schedule)
        elif schedule.repeat_every_x_months:
            schedule.day_planned_to_complete = (
                schedule.day_planned_to_complete
                + timedelta(weeks=schedule.repeat_every_x_months * 4)
            )
            if schedule.day_planned_to_complete <= date.today():
                schedule.day_planned_to_complete = date.today() + timedelta(
                    weeks=schedule.repeat_every_x_months * 4
                )
            await schedule_repository.persist(schedule)
        else:
            await schedule_repository.remove(schedule)


async def add_new_task(new_task: str):
    task_repository = repositories.TodoTaskRepository()
    task = entities.TodoTask(name=new_task)
    await task_repository.persist(task)


async def get_schedules() -> list[entities.TodoTaskSchedule]:
    schedule_repository = repositories.TodoTaskScheduleRepository()
    return await schedule_repository.get_list()


async def create_schedule(validated_form_data: dict) -> entities.TodoTaskSchedule:
    schedule_repository = repositories.TodoTaskScheduleRepository()
    schedule = entities.TodoTaskSchedule(**validated_form_data)
    await schedule_repository.persist(schedule)
    return schedule


async def update_schedule(
    schedule: entities.TodoTaskSchedule, validated_form_data: dict
) -> entities.TodoTaskSchedule:
    schedule_repository = repositories.TodoTaskScheduleRepository()
    schedule = entities.TodoTaskSchedule(**validated_form_data, id=schedule.id)
    await schedule_repository.persist(schedule)
    return schedule


async def get_schedule_by_id(schedule_id: int) -> entities.TodoTaskSchedule | None:
    schedule_repository = repositories.TodoTaskScheduleRepository()
    return await schedule_repository.get_by_id(schedule_id)


async def get_task_by_id(task_id: int) -> entities.TodoTask | None:
    repository = repositories.TodoTaskRepository()
    task = await repository.get_by_id(task_id)

    if not task:
        raise ValidationError("Task does not exist!")

    if task.is_completed:
        raise ValidationError("Task was already completed!")

    assert task.id
    return task
