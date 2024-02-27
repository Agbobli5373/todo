from datetime import date
from todos.tasks import create_tasks_for_today

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
            return_value=unfinished_tasks,
        )
        schedules = [
            factories.TodoTaskScheduleFactory.build(id=id) for id in range(6, 9)
        ]
        mock_get_schedules = mocker.patch.object(
            repositories.TodoTaskScheduleRepository,
            "get_scheduled_for_day",
            return_value=schedules,
        )
        mock_persist = mocker.patch.object(
            repositories.TodoTaskRepository, "persist_all"
        )

        create_tasks_for_today()

        mock_get_schedules.assert_called_once_with(
            date.today(), exclude_ids=[task.schedule_id for task in unfinished_tasks]
        )
        mock_persist.assert_called_once_with(
            [
                entities.TodoTask(
                    name=scheduled_task.name,
                    schedule_id=scheduled_task.id,
                )
                for scheduled_task in schedules
            ]
        )
