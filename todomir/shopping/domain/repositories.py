from django.db.models import QuerySet
from shopping.domain import entities
from shopping import models


class ShoppingListItemRepository:
    async def get_list(self) -> list[entities.ShoppingListItem]:
        queryset = models.ShoppingListItem.objects.all()
        return await self._map_from_query(queryset)

    async def persist(self, entity: entities.ShoppingListItem):
        if entity.id:
            instance = await models.ShoppingListItem.objects.aget(id=entity.id)
        else:
            instance = models.ShoppingListItem()

        instance.name = entity.name
        instance.completed = entity.completed
        await instance.asave()

        entity.id = instance.id

    async def get_by_id(self, item_id: int) -> entities.ShoppingListItem | None:
        try:
            instance = await models.ShoppingListItem.objects.aget(id=item_id)
        except models.ShoppingListItem.DoesNotExist:
            return None
        else:
            return self._map_from_instance(instance)

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
