import pytest
from datetime import datetime, date, timedelta
from unittest.mock import AsyncMock
from todos.domain import repositories, services
import time_machine


from todos.tests import factories


@pytest.mark.asyncio
class TestCompleteTask:
    @time_machine.travel(datetime(2022, 2, 2), tick=False)
    async def test_without_schedule(self, mocker, faker):
        """Should remove the task if its completed and doesnt have schedule"""
        task = factories.TodoTaskFactory.build(
            id=faker.pyint(), schedule_id=None, completed=None
        )
        mock_persist = mocker.patch.object(
            repositories.TodoTaskRepository, "persist", new=AsyncMock()
        )
        mock_get_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository,
            "get_by_id",
            new=AsyncMock(),
        )

        await services.complete_task(task)

        mock_get_schedule.assert_not_called()
        assert task.completed == datetime.now()
        mock_persist.assert_called_once_with(task)

    @time_machine.travel(datetime(2022, 2, 2), tick=False)
    async def test_with_no_repeatable_schedule(self, mocker, faker):
        """Should remove the task and its schedule if the schedule is not repeatable"""
        task = factories.TodoTaskFactory.build(
            id=faker.pyint(),
            schedule_id=faker.pyint(),
            completed=None,
        )
        schedule = factories.TodoTaskScheduleFactory.build(
            id=task.schedule_id,
            repeat_every_x_days=None,
            repeat_every_x_weeks=None,
            repeat_every_x_months=None,
        )
        mock_get_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository,
            "get_by_id",
            new=AsyncMock(return_value=schedule),
        )
        mock_remove_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository, "remove", new=AsyncMock()
        )
        mock_persist = mocker.patch.object(
            repositories.TodoTaskRepository, "persist", new=AsyncMock()
        )

        await services.complete_task(task)

        mock_get_schedule.assert_called_once_with(task.schedule_id)
        assert task.completed == datetime.now()
        mock_persist.assert_called_once_with(task)
        mock_remove_schedule.assert_called_once_with(schedule)

    @time_machine.travel(datetime(2022, 2, 2), tick=False)
    async def test_with_repeatable_schedule_by_days(self, mocker, faker):
        """Should remove the task and update schedule next day."""
        task = factories.TodoTaskFactory.build(
            id=faker.pyint(),
            schedule_id=faker.pyint(),
            completed=None,
        )
        schedule = factories.TodoTaskScheduleFactory.build(
            id=task.schedule_id,
            day_planned_to_complete=date.today(),
            repeat_every_x_days=2,
            repeat_every_x_weeks=None,
            repeat_every_x_months=None,
        )
        mock_get_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository,
            "get_by_id",
            new=AsyncMock(return_value=schedule),
        )
        mock_remove_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository, "remove", new=AsyncMock()
        )
        mock_persist_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository, "persist", new=AsyncMock()
        )
        mock_persist_task = mocker.patch.object(
            repositories.TodoTaskRepository, "persist", new=AsyncMock()
        )

        await services.complete_task(task)

        mock_get_schedule.assert_called_once_with(task.schedule_id)
        assert task.completed == datetime.now()
        assert schedule.day_planned_to_complete == date.today() + timedelta(days=2)
        mock_persist_task.assert_called_once_with(task)
        mock_remove_schedule.assert_not_called()
        mock_persist_schedule.assert_called_with(schedule)

    @time_machine.travel(datetime(2022, 2, 2), tick=False)
    async def test_with_repeatable_schedule_by_weeks(self, mocker, faker):
        """
        Should remove the task and update schedule next day.
        In case of `repeat_every_x_days` next day should be moved relative to the current day.
        but in other cases it should be moved relative to preiovus planned day - exception to this
        is case when task was completed overdue for longer periodthan repeat frequency.
        """
        task = factories.TodoTaskFactory.build(
            id=faker.pyint(),
            schedule_id=faker.pyint(),
            completed=None,
        )
        initial_date = date.today() - timedelta(days=1)
        schedule = factories.TodoTaskScheduleFactory.build(
            id=task.schedule_id,
            day_planned_to_complete=initial_date,
            repeat_every_x_days=None,
            repeat_every_x_weeks=2,
            repeat_every_x_months=None,
        )
        mock_get_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository,
            "get_by_id",
            new=AsyncMock(return_value=schedule),
        )
        mock_remove_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository, "remove", new=AsyncMock()
        )
        mock_persist_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository, "persist", new=AsyncMock()
        )
        mock_persist_task = mocker.patch.object(
            repositories.TodoTaskRepository, "persist", new=AsyncMock()
        )

        await services.complete_task(task)

        mock_get_schedule.assert_called_once_with(task.schedule_id)
        assert task.completed == datetime.now()
        assert schedule.day_planned_to_complete == initial_date + timedelta(weeks=2)
        mock_persist_task.assert_called_once_with(task)
        mock_remove_schedule.assert_not_called()
        mock_persist_schedule.assert_called_with(schedule)

    @time_machine.travel(datetime(2022, 2, 2), tick=False)
    async def test_with_repeatable_schedule_by_weeks_overdue(self, mocker, faker):
        task = factories.TodoTaskFactory.build(
            id=faker.pyint(),
            schedule_id=faker.pyint(),
            completed=None,
        )
        initial_date = date.today() - timedelta(weeks=3)
        schedule = factories.TodoTaskScheduleFactory.build(
            id=task.schedule_id,
            day_planned_to_complete=initial_date,
            repeat_every_x_days=None,
            repeat_every_x_weeks=2,
            repeat_every_x_months=None,
        )
        mock_get_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository,
            "get_by_id",
            new=AsyncMock(return_value=schedule),
        )
        mock_remove_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository,
            "remove",
            new=AsyncMock(),
        )
        mock_persist_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository,
            "persist",
            new=AsyncMock(),
        )
        mock_persist_task = mocker.patch.object(
            repositories.TodoTaskRepository,
            "persist",
            new=AsyncMock(),
        )

        await services.complete_task(task)

        mock_get_schedule.assert_called_once_with(task.schedule_id)
        assert task.completed == datetime.now()
        assert schedule.day_planned_to_complete == initial_date + timedelta(weeks=4)
        mock_persist_task.assert_called_once_with(task)
        mock_remove_schedule.assert_not_called()
        mock_persist_schedule.assert_called_with(schedule)
