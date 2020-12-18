from sqlalchemy import Column, Integer, String, MetaData, Table

from .database import engine


metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', String),
    Column('age', Integer)
)

metadata.create_all(engine)

