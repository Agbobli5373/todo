from datetime import datetime, timedelta, date

from todos.domain import entities, repositories, exceptions


async def get_tasks() -> list[entities.TodoTask]:
    repository = repositories.TodoTaskRepository()
    return await repository.get_list()


async def complete_task(task: entities.TodoTask):
    if task.completed:
        raise exceptions.TaskAlreadyCompleted

    task_repository = repositories.TodoTaskRepository()

    task.completed = datetime.now()
    await task_repository.persist(task)

    schedule_repository = repositories.TodoTaskScheduleRepository()
    if task.schedule_id and (
        schedule := await schedule_repository.get_by_id(task.schedule_id)
    ):
        frequency_in_days = schedule.frequency_days
        if frequency_in_days == 0:
            await schedule_repository.remove(schedule)
            return

        target_date = schedule.day_planned_to_complete
        while target_date <= date.today():
            target_date = target_date + timedelta(days=frequency_in_days)

        schedule.day_planned_to_complete = target_date
        await schedule_repository.persist(schedule)


async def undo_task(task: entities.TodoTask):
    if not task.completed:
        raise exceptions.TaskNotCompletedYet

    task_repository = repositories.TodoTaskRepository()

    task.completed = None
    await task_repository.persist(task)

    schedule_repository = repositories.TodoTaskScheduleRepository()
    if task.schedule_id and (
        schedule := await schedule_repository.get_by_id(task.schedule_id)
    ):
        frequency_in_days = schedule.frequency_days

        schedule.day_planned_to_complete = schedule.day_planned_to_complete - timedelta(
            days=frequency_in_days
        )
        await schedule_repository.persist(schedule)


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

    if not task or not task.id:
        raise exceptions.TaskNotFound

    return task
