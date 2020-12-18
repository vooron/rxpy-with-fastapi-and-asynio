from typing import List

from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True


class PagedUser(BaseModel):
    count: int
    limit: int
    offset: int
    data: List[User]
