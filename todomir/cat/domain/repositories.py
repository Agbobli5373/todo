import httpx

from cat.domain import entities


class CatRepository:
    async def get_random(self) -> entities.Cat:
        url = "https://api.thecatapi.com/v1/images/search"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        return entities.Cat(**response.json()[0])
