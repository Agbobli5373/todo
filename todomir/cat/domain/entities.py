from pydantic import BaseModel


class Cat(BaseModel):
    id: str
    url: str
    width: int
    height: int
