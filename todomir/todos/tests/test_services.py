from datetime import datetime, date, timedelta
from todos.domain import repositories, services
import time_machine


from todos.tests import factories


class TestCompleteTask:
    @time_machine.travel(datetime(2022, 2, 2), tick=False)
    def test_without_schedule(self, mocker, faker):
        """Should remove the task if its completed and doesnt have schedule"""
        task = factories.TodoTaskFactory.build(id=faker.pyint(), schedule_id=None)
        assert task.id
        mock_get_by_id = mocker.patch.object(
            repositories.TodoTaskRepository,
            "get_by_id",
            return_value=task,
        )
        mock_persist = mocker.patch.object(
            repositories.TodoTaskRepository,
            "persist",
        )
        mock_get_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository,
            "get_by_id",
        )

        services.complete_task(task.id)

        mock_get_by_id.assert_called_once_with(task.id)
        mock_get_schedule.assert_not_called()
        assert task.completed_at == datetime.now()
        mock_persist.assert_called_once_with(task)

    @time_machine.travel(datetime(2022, 2, 2), tick=False)
    def test_with_no_repeatable_schedule(self, mocker, faker):
        """Should remove the task and its schedule if the schedule is not repeatable"""
        task = factories.TodoTaskFactory.build(
            id=faker.pyint(), schedule_id=faker.pyint()
        )
        schedule = factories.TodoTaskScheduleFactory.build(
            id=task.schedule_id,
            repeat_every_x_days=None,
            repeat_every_x_weeks=None,
            repeat_every_x_months=None,
        )
        assert task.id
        mock_get_by_id = mocker.patch.object(
            repositories.TodoTaskRepository,
            "get_by_id",
            return_value=task,
        )
        mock_get_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository,
            "get_by_id",
            return_value=schedule,
        )
        mock_remove_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository,
            "remove",
        )
        mock_persist = mocker.patch.object(
            repositories.TodoTaskRepository,
            "persist",
        )

        services.complete_task(task.id)

        mock_get_by_id.assert_called_once_with(task.id)
        mock_get_schedule.assert_called_once_with(task.schedule_id)
        assert task.completed_at == datetime.now()
        mock_persist.assert_called_once_with(task)
        mock_remove_schedule.assert_called_once_with(schedule)

    @time_machine.travel(datetime(2022, 2, 2), tick=False)
    def test_with_repeatable_schedule_by_days(self, mocker, faker):
        """Should remove the task and update schedule next day."""
        task = factories.TodoTaskFactory.build(
            id=faker.pyint(), schedule_id=faker.pyint()
        )
        schedule = factories.TodoTaskScheduleFactory.build(
            id=task.schedule_id,
            repeat_every_x_days=2,
            repeat_every_x_weeks=None,
            repeat_every_x_months=None,
        )
        assert task.id
        mock_get_by_id = mocker.patch.object(
            repositories.TodoTaskRepository, "get_by_id", return_value=task
        )
        mock_get_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository, "get_by_id", return_value=schedule
        )
        mock_remove_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository, "remove"
        )
        mock_persist_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository, "persist"
        )
        mock_persist_task = mocker.patch.object(
            repositories.TodoTaskRepository, "persist"
        )

        services.complete_task(task.id)

        mock_get_by_id.assert_called_once_with(task.id)
        mock_get_schedule.assert_called_once_with(task.schedule_id)
        assert task.completed_at == datetime.now()
        assert schedule.day_planned_to_complete == date.today() + timedelta(days=2)
        mock_persist_task.assert_called_once_with(task)
        mock_remove_schedule.assert_not_called()
        mock_persist_schedule.assert_called_with(schedule)

    @time_machine.travel(datetime(2022, 2, 2), tick=False)
    def test_with_repeatable_schedule_by_weeks(self, mocker, faker):
        """
        Should remove the task and update schedule next day.
        In case of `repeat_every_x_days` next day should be moved relative to the current day.
        but in other cases it should be moved relative to preiovus planned day - exception to this
        is case when task was completed overdue for longer periodthan repeat frequency.
        """
        task = factories.TodoTaskFactory.build(
            id=faker.pyint(), schedule_id=faker.pyint()
        )
        initial_date = date.today() - timedelta(days=1)
        schedule = factories.TodoTaskScheduleFactory.build(
            id=task.schedule_id,
            day_planned_to_complete=initial_date,
            repeat_every_x_days=None,
            repeat_every_x_weeks=2,
            repeat_every_x_months=None,
        )
        assert task.id
        mock_get_by_id = mocker.patch.object(
            repositories.TodoTaskRepository, "get_by_id", return_value=task
        )
        mock_get_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository, "get_by_id", return_value=schedule
        )
        mock_remove_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository, "remove"
        )
        mock_persist_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository, "persist"
        )
        mock_persist_task = mocker.patch.object(
            repositories.TodoTaskRepository, "persist"
        )

        services.complete_task(task.id)

        mock_get_by_id.assert_called_once_with(task.id)
        mock_get_schedule.assert_called_once_with(task.schedule_id)
        assert task.completed_at == datetime.now()
        assert schedule.day_planned_to_complete == initial_date + timedelta(weeks=2)
        mock_persist_task.assert_called_once_with(task)
        mock_remove_schedule.assert_not_called()
        mock_persist_schedule.assert_called_with(schedule)

    @time_machine.travel(datetime(2022, 2, 2), tick=False)
    def test_with_repeatable_schedule_by_weeks_overdue(self, mocker, faker):
        """
        If the task was completed overdue for longer period than repeat frequency,
        then next day should be set relative to today.
        """
        task = factories.TodoTaskFactory.build(
            id=faker.pyint(), schedule_id=faker.pyint()
        )
        initial_date = date.today() - timedelta(weeks=3)
        schedule = factories.TodoTaskScheduleFactory.build(
            id=task.schedule_id,
            day_planned_to_complete=initial_date,
            repeat_every_x_days=None,
            repeat_every_x_weeks=2,
            repeat_every_x_months=None,
        )
        assert task.id
        mock_get_by_id = mocker.patch.object(
            repositories.TodoTaskRepository, "get_by_id", return_value=task
        )
        mock_get_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository, "get_by_id", return_value=schedule
        )
        mock_remove_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository, "remove"
        )
        mock_persist_schedule = mocker.patch.object(
            repositories.TodoTaskScheduleRepository, "persist"
        )
        mock_persist_task = mocker.patch.object(
            repositories.TodoTaskRepository, "persist"
        )

        services.complete_task(task.id)

        mock_get_by_id.assert_called_once_with(task.id)
        mock_get_schedule.assert_called_once_with(task.schedule_id)
        assert task.completed_at == datetime.now()
        assert schedule.day_planned_to_complete == date.today() + timedelta(weeks=2)
        mock_persist_task.assert_called_once_with(task)
        mock_remove_schedule.assert_not_called()
        mock_persist_schedule.assert_called_with(schedule)
