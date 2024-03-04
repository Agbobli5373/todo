from django.utils import timezone
from shopping.domain import entities, repositories, exceptions


async def get_all_items() -> list[entities.ShoppingListItem]:
    repository = repositories.ShoppingListItemRepository()
    return await repository.get_list()


async def add_new_item(name: str) -> entities.ShoppingListItem:
    repository = repositories.ShoppingListItemRepository()
    entity = entities.ShoppingListItem(name=name, created=timezone.now())
    await repository.persist(entity)
    return entity


async def complete_item(item_id: int):
    repository = repositories.ShoppingListItemRepository()
    item = await repository.get_by_id(item_id)
    if not item:
        raise exceptions.ShoppingListItemNotFound

    item.completed = timezone.now()
    await repository.persist(item)


async def undo_item(item_id: int):
    repository = repositories.ShoppingListItemRepository()
    item = await repository.get_by_id(item_id)
    if not item:
        raise exceptions.ShoppingListItemNotFound

    item.completed = None
    await repository.persist(item)
