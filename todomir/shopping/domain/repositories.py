from typing import Type
from django.db.models import QuerySet
from shopping.domain import entities
from shopping import models
from common.domain import repositories


class ShoppingListItemRepository(
    repositories.Repository[models.ShoppingListItem, entities.ShoppingListItem]
):
    @property
    def model(self) -> Type[models.ShoppingListItem]:
        return models.ShoppingListItem

    def _map_from_instance(
        self, instance: models.ShoppingListItem
    ) -> entities.ShoppingListItem:
        return entities.ShoppingListItem(
            id=instance.id,
            name=instance.name,
            completed=instance.completed,
            created=instance.created,
        )

    async def _map_from_query(
        self, queryset: QuerySet
    ) -> list[entities.ShoppingListItem]:
        return [self._map_from_instance(instance) async for instance in queryset]

    def _update_instance_with_entity_values(
        self, instance: models.ShoppingListItem, entity: entities.ShoppingListItem
    ):
        instance.name = entity.name
        instance.completed = entity.completed
        instance.created = entity.created
