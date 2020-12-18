import requests
from faker import Faker

from filia.schemas import User

faker = Faker()

DATA_AMOUNT = 500
HOST = 'http://127.0.0.1:8000'

data = [User(name=faker.name(), age=faker.random_int(10, 100)).dict() for _ in range(DATA_AMOUNT)]

r = requests.post(HOST + "/batch/users/", json=data)

print("Status:", r.status_code)
print("Response:", r.json())
