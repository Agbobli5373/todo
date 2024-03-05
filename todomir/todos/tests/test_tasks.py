from datetime import date, datetime
from unittest.mock import AsyncMock
import time_machine
from todos.integrations.wastes import SCHEDULE_MIXED_WASTES, SCHEDULE_SEGREGATED_WASTES
from todos.tasks import create_tasks_for_today
from todos.integrations.tasks import create_task_to_prepare_wastes

from todos.domain import repositories, entities

from todos.tests import factories


class TestCreateTasksForToday:
    def test_should_create_scheduled_tasks(self, mocker):
        unfinished_tasks = [
            factories.TodoTaskFactory.build(schedule_id=id) for id in range(1, 5)
        ]
        mocker.patch.object(
            repositories.TodoTaskRepository,
            "get_unfinished",
            new=AsyncMock(return_value=unfinished_tasks),
        )
        schedules = [
            factories.TodoTaskScheduleFactory.build(id=id) for id in range(6, 9)
        ]
        mock_get_schedules = mocker.patch.object(
            repositories.TodoTaskScheduleRepository,
            "get_scheduled_for_day",
            new=AsyncMock(return_value=schedules),
        )
        mock_bulk_create = mocker.patch.object(
            repositories.TodoTaskRepository, "bulk_create", new=AsyncMock()
        )

        create_tasks_for_today()

        mock_get_schedules.assert_called_once_with(
            date.today(), exclude_ids=[task.schedule_id for task in unfinished_tasks]
        )
        mock_bulk_create.assert_called_once_with(
            [
                entities.TodoTask(
                    name=scheduled_task.name,
                    schedule_id=scheduled_task.id,
                )
                for scheduled_task in schedules
            ]
        )


class TestCreateTasksToPrepareWastes:
    @time_machine.travel(datetime(2024, 4, 12), tick=False)
    def test_should_create_segregated(self, mocker):
        mocker.patch.dict(SCHEDULE_SEGREGATED_WASTES, {2024: {4: [5, 13]}})
        mocker.patch.dict(SCHEDULE_MIXED_WASTES, {2024: {5: [1, 13]}})
        mock_persist = mocker.patch.object(
            repositories.TodoTaskRepository, "persist", new=AsyncMock()
        )

        create_task_to_prepare_wastes()

        mock_persist.assert_called_once_with(
            entities.TodoTask(name="Wystawić śmieci segregowane")
        )

    @time_machine.travel(datetime(2024, 5, 19), tick=False)
    def test_should_create_mixed(self, mocker):
        mocker.patch.dict(SCHEDULE_SEGREGATED_WASTES, {2024: {4: [5, 20]}})
        mocker.patch.dict(SCHEDULE_MIXED_WASTES, {2024: {5: [1, 20]}})
        mock_persist = mocker.patch.object(
            repositories.TodoTaskRepository, "persist", new=AsyncMock()
        )

        create_task_to_prepare_wastes()

        mock_persist.assert_called_once_with(
            entities.TodoTask(name="Wystawić kubeł na śmieci mieszane")
        )
