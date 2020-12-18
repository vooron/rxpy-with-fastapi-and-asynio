import databases
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
database = databases.Database(SQLALCHEMY_DATABASE_URL)
