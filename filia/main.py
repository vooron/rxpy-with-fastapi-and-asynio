from fastapi import FastAPI

from . import schemas
from .database import database
from .models import users

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/users/")
async def create_user(user: schemas.User):
    query = users.insert().values(name=user.name, age=user.age)
    created_id = await database.execute(query)
    return {**user.dict(), "id": created_id}


@app.get("/users/", response_model=schemas.PagedUser)
async def read_users(skip: int = 0, limit: int = 100):
    users_query = users.select().offset(skip).limit(limit)
    count_query = users.select().count()

    db_users = await database.fetch_all(users_query)
    count = await database.fetch_val(count_query)

    return schemas.PagedUser(
        count=count,
        limit=limit,
        offset=skip,
        data=db_users
    )
