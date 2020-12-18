from typing import List

import requests
import rx
from fastapi import FastAPI
from rx import operators as op

from main_office import schemas
from main_office.services import get_all_users

app = FastAPI()

config = dict(
    servers={  # sharding servers
        "Server 1": dict(
            address="http://filia_1:8000"
        ),
        "Server 2": dict(
            address="http://filia_2:8000"
        )
    },
    sharding_rules=dict(
        users=lambda user: "Server 1" if user.age < 45 else "Server 2"
    )
)


@app.post("/batch/users/")
def create_users(users: List[schemas.User]):
    stream = rx.from_list(users).pipe(
        op.map(lambda user: (user, config["sharding_rules"]['users'](user)))
    )

    stream.subscribe(
        on_next=lambda i: requests.post(config['servers'][i[1]]['address'] + "/users/", json=i[0].dict()),
        on_error=lambda e: print("Error Occurred: {0}".format(e)),
        on_completed=lambda: print("Done!")
    )


@app.get("/batch/users/", response_model=List[schemas.User])
def read_users():
    return get_all_users()
