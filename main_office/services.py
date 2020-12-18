import asyncio
from typing import List

import requests
import rx
from rx.subject import Subject

from main_office.schemas import PagedUser, User


async def fetch_pages(observer: Subject, i: int, uri: str, page_size: int):
    r = requests.get(uri + f"?skip={i * page_size}&limit={page_size}")
    payload = PagedUser(**r.json())

    for user in payload.data:
        observer.on_next(user)


async def fetch_from_specific_server(observer: Subject, uri: str, page_size: int):
    r = requests.get(uri + f"?skip=0&limit={page_size}")

    payload = PagedUser(**r.json())

    for user in payload.data:
        observer.on_next(user)

    await asyncio.gather(*[fetch_pages(observer, i, uri, page_size) for i in range(1, payload.count // page_size)])


def fetch_all_users(observer: Subject, scheduler):
    from main_office.main import config
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []
    for server in config['servers'].values():
        tasks.append(
            fetch_from_specific_server(observer, server['address'] + "/users/", 100)
        )
    loop.run_until_complete(asyncio.gather(*tasks))
    observer.on_completed()


def get_all_users() -> List[User]:
    stream = rx.create(fetch_all_users)

    result = []

    stream.subscribe(
        on_next=lambda i: result.append(i),
        on_error=lambda e: print("Error Occurred: {0}".format(e)),
        on_completed=lambda: print("Done!")
    )

    return result
