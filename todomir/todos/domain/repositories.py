from datetime import date
from django.db import transaction
from django.db.models import QuerySet
from todos.database import models

from todos.domain import entities


class TodoTaskRepository:
    def get_by_id(self, id: int) -> entities.TodoTask | None:
        try:
            instance = models.TodoTask.objects.get(id=id)
            return self._map_from_instance(instance)
        except models.TodoTask.DoesNotExist:
            return None

    def get_list(self) -> list[entities.TodoTask]:
        queryset = models.TodoTask.objects.all().order_by(
            "completed", "day_planned_to_complete"
        )
        return self._map_from_query(queryset)

    def get_finished(self) -> list[entities.TodoTask]:
        queryset = models.TodoTask.objects.filter(completed__isnull=False)
        return self._map_from_query(queryset)

    def get_unfinished(self) -> list[entities.TodoTask]:
        queryset = models.TodoTask.objects.filter(
            schedule__isnull=False, completed__isnull=True
        )
        return self._map_from_query(queryset)

    def persist(self, entity: entities.TodoTask) -> None:
        if entity.id:
            instance = models.TodoTask.objects.get(id=entity.id)
        else:
            instance = models.TodoTask()

        instance.name = entity.name
        instance.completed = entity.completed_at
        if not instance.day_planned_to_complete:
            instance.day_planned_to_complete = date.today()
        instance.save()

    @transaction.atomic
    def persist_all(self, entities: list[entities.TodoTask]) -> None:
        for entity in entities:
            self.persist(entity)

    def remove_all(self, entities: list[entities.TodoTask]) -> None:
        models.TodoTask.objects.filter(
            id__in=[entity.id for entity in entities]
        ).delete()

    def _map_from_query(self, query: QuerySet) -> list[entities.TodoTask]:
        return [
            entities.TodoTask(
                id=instance.pk,
                name=instance.name,
                is_overdue=instance.is_overdue,
                is_completed=instance.completed is not None,
                completed_at=instance.completed,
                schedule_id=instance.schedule_id if instance.schedule_id else None,
            )
            for instance in query
        ]

    def _map_from_instance(self, instance: models.TodoTask) -> entities.TodoTask:
        today = date.today()
        return entities.TodoTask(
            id=instance.pk,
            name=instance.name,
            is_overdue=instance.day_planned_to_complete < today,
            is_completed=instance.completed is not None,
            completed_at=instance.completed,
            schedule_id=instance.schedule_id if instance.schedule_id else None,
        )


class TodoTaskScheduleRepository:
    def get_scheduled_for_day(
        self, day: date, exclude_ids: list[int] | None = None
    ) -> list[entities.TodoTaskSchedule]:
        queryset = models.TodoTaskSchedule.objects.filter(day_planned_to_complete=day)
        if exclude_ids:
            queryset = queryset.exclude(pk__in=exclude_ids)

        return self._map_from_query(queryset)

    def get_by_id(self, id: int) -> entities.TodoTaskSchedule | None:
        try:
            instance = models.TodoTaskSchedule.objects.get(id=id)
            return self._map_from_instance(instance)
        except models.TodoTask.DoesNotExist:
            return None

    def persist(self, entity: entities.TodoTaskSchedule) -> None:
        if entity.id:
            instance = models.TodoTaskSchedule.objects.get(id=entity.id)
        else:
            instance = models.TodoTaskSchedule()

        instance.name = entity.name
        instance.completed = entity.completed_at
        instance.day_planned_to_complete = entity.day_planned_to_complete
        instance.repeat_every_x_days = entity.repeat_every_x_days
        instance.repeat_every_x_weeks = entity.repeat_every_x_week
        instance.repeat_every_x_months = entity.repeat_every_x_months
        instance.save()

    def remove(self, entity: entities.TodoTaskSchedule) -> None:
        models.TodoTaskSchedule.objects.filter(id=entity.id).delete()

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

    def _map_from_query(self, query: QuerySet) -> list[entities.TodoTaskSchedule]:
        return [self._map_from_instance(instance) for instance in query]
