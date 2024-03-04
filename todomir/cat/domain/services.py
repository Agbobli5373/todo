from cat.domain import repositories, entities


async def get_cat() -> entities.Cat:
    repository = repositories.CatRepository()
    return await repository.get_random()
