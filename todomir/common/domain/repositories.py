from typing import TypeVar, Generic, Type
from abc import ABC, abstractmethod

from django.db import models
from common.domain import entities

T = TypeVar("T", bound=models.Model)
V = TypeVar("V", bound=entities.DbEntity)


class Repository(Generic[T, V], ABC):
    @property
    @abstractmethod
    def model(self) -> Type[T]:
        ...

    @abstractmethod
    def _map_from_instance(self, instance: T) -> V:
        ...

    @abstractmethod
    async def _map_from_query(self, queryset: models.QuerySet) -> list[V]:
        ...

    @abstractmethod
    def _update_instance_with_entity_values(self, instance: T, entity: V):
        ...

    def get_queryset(self) -> models.QuerySet:
        return self.model.objects.all()

    async def get_by_id(self, id: int) -> V:
        try:
            instance = await self.model.objects.aget(id=id)
            return self._map_from_instance(instance)
        except self.model.DoesNotExist:
            return None

    async def get_list(self) -> list[V]:
        return await self._map_from_query(self.get_queryset())

    async def persist(self, entity: V) -> None:
        if entity.id:
            instance = instance = await self.model.objects.aget(id=entity.id)
        else:
            instance = self.model()

        self._update_instance_with_entity_values(instance, entity)
        await instance.asave()
        entity.id = instance.id

    async def bulk_create(self, entities: list[V]) -> None:
        batch = []
        for entity in entities:
            instance = self.model()
            self._update_instance_with_entity_values(instance, entity)
            batch.append(instance)

        await self.model.objects.abulk_create(batch)

    async def remove_all(self, entities: list[V]) -> None:
        await (
            self.get_queryset()
            .filter(id__in=[entity.id for entity in entities])
            .adelete()
        )

    async def remove(self, entity: V) -> None:
        await self.get_queryset().filter(id=entity.id).adelete()
