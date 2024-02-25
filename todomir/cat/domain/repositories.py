import requests

from cat.domain import entities


class CatRepository:
    def get_random(self) -> entities.Cat:
        url = "https://api.thecatapi.com/v1/images/search"
        response = requests.get(url)
        return entities.Cat(**response.json()[0])
