from cat.domain import repositories, entities


def get_cat() -> entities.Cat:
    repository = repositories.CatRepository()
    return repository.get_random()
