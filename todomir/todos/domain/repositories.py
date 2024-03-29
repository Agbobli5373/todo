from typing import Type
from datetime import date
from django.db.models import QuerySet
from todos.database import models

from todos.domain import entities
from common.domain import repositories


class TodoTaskRepository(repositories.Repository[models.TodoTask, entities.TodoTask]):
    @property
    def model(self) -> Type[models.TodoTask]:
        return models.TodoTask

    def get_queryset(self) -> QuerySet:
        return self.model.objects.all().order_by(
            "completed", "day_planned_to_complete", "-id"
        )

    async def get_by_external_id(self, external_id: str) -> entities.TodoTask | None:
        try:
            instance = await models.TodoTask.objects.aget(external_id=external_id)
            return self._map_from_instance(instance)
        except models.TodoTask.DoesNotExist:
            return None

    async def get_finished(self) -> list[entities.TodoTask]:
        queryset = models.TodoTask.objects.filter(completed__isnull=False)
        return await self._map_from_query(queryset)

    async def get_unfinished(self) -> list[entities.TodoTask]:
        queryset = models.TodoTask.objects.filter(
            schedule__isnull=False, completed__isnull=True
        )
        return await self._map_from_query(queryset)

    async def remove_all_finished(self) -> None:
        await models.TodoTask.objects.filter(completed__isnull=False).adelete()

    def _update_instance_with_entity_values(
        self, instance: models.TodoTask, entity: entities.TodoTask
    ):
        instance.name = entity.name
        instance.completed = entity.completed
        instance.schedule_id = entity.schedule_id
        instance.external_id = entity.external_id
        if not instance.day_planned_to_complete:
            instance.day_planned_to_complete = date.today()

    async def _map_from_query(self, queryset: QuerySet) -> list[entities.TodoTask]:
        return [
            entities.TodoTask(
                id=instance.pk,
                name=instance.name,
                is_overdue=instance.is_overdue,
                completed=instance.completed,
                schedule_id=instance.schedule_id if instance.schedule_id else None,
            )
            async for instance in queryset
        ]

    def _map_from_instance(self, instance: models.TodoTask) -> entities.TodoTask:
        today = date.today()
        return entities.TodoTask(
            id=instance.pk,
            name=instance.name,
            is_overdue=instance.day_planned_to_complete < today,
            completed=instance.completed,
            schedule_id=instance.schedule_id if instance.schedule_id else None,
        )


class TodoTaskScheduleRepository(
    repositories.Repository[models.TodoTaskSchedule, entities.TodoTaskSchedule]
):
    @property
    def model(self) -> Type[models.TodoTaskSchedule]:
        return models.TodoTaskSchedule

    def get_queryset(self) -> QuerySet:
        return self.model.objects.all().order_by("day_planned_to_complete")

    async def get_scheduled_for_day(
        self, day: date, exclude_ids: list[int] | None = None
    ) -> list[entities.TodoTaskSchedule]:
        queryset = models.TodoTaskSchedule.objects.filter(day_planned_to_complete=day)
        if exclude_ids:
            queryset = queryset.exclude(pk__in=exclude_ids)

        return await self._map_from_query(queryset)

    async def remove_all_finished(self) -> None:
        await models.TodoTaskSchedule.objects.filter(
            day_planned_to_complete__lt=date.today()
        ).adelete()

    def _update_instance_with_entity_values(
        self, instance: models.TodoTaskSchedule, entity: entities.TodoTaskSchedule
    ):
        instance.name = entity.name
        instance.day_planned_to_complete = entity.day_planned_to_complete
        instance.repeat_every_x_days = entity.repeat_every_x_days
        instance.repeat_every_x_weeks = entity.repeat_every_x_weeks
        instance.repeat_every_x_months = entity.repeat_every_x_months

    def _map_from_instance(
        self, instance: models.TodoTaskSchedule
    ) -> entities.TodoTaskSchedule:
        return entities.TodoTaskSchedule(
            id=instance.pk,
            name=instance.name,
            day_planned_to_complete=instance.day_planned_to_complete,
            repeat_every_x_days=instance.repeat_every_x_days,
            repeat_every_x_weeks=instance.repeat_every_x_weeks,
            repeat_every_x_months=instance.repeat_every_x_months,
        )

    async def _map_from_query(
        self, queryset: QuerySet
    ) -> list[entities.TodoTaskSchedule]:
        return [self._map_from_instance(instance) async for instance in queryset]
