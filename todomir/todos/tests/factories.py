from polyfactory.factories.pydantic_factory import ModelFactory
from freezegun.api import FakeDatetime, FakeDate
from typing import Type, Any

from todos.domain.entities import TodoTask, TodoTaskSchedule


class TodoTaskFactory(ModelFactory[TodoTask]):
    @classmethod
    def get_provider_map(cls) -> dict[Type, Any]:
        providers_map = super().get_provider_map()

        return {
            FakeDatetime: cls.__faker__.date_time,
            FakeDate: cls.__faker__.date_object,
            **providers_map,
        }


class TodoTaskScheduleFactory(ModelFactory[TodoTaskSchedule]):
    @classmethod
    def get_provider_map(cls) -> dict[Type, Any]:
        providers_map = super().get_provider_map()

        return {
            FakeDatetime: cls.__faker__.date_time,
            FakeDate: cls.__faker__.date_object,
            **providers_map,
        }
