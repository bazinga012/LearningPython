# import random
import asyncio
from time import time

# from aiohttp import ClientSession


async def fetch(async_request, session):
    async with async_request.call_session_request(session) as response:
        return await response.text()


async def bound_fetch(sem, async_request, session):
    # Getter function with semaphore.
    async with sem:
        return await fetch(async_request, session)


def task_done_handler(task):
    print("callback called")
    task_exception = task.exception()
    if task_exception is None:
        task.async_request.success_handler(task.result())
    else:
        task.async_request.error_handler(task_exception)


class AsyncRequest():
    def __init__(self, url, http_method, params=None, payload=None, headers=None):
        self.url = url
        self.http_method = http_method
        self.params = params or {}
        self.payload = payload
        self.headers = headers or {}

    def call_session_request(self, session):
        return getattr(session, self.http_method)(self.url, params=self.params, headers=self.headers, json=self.payload)

    def success_handler(self, response):
        print(response)

    def error_handler(self, error):
        print(error)


async def run(async_requests):
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(10)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for async_request in async_requests:
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, async_request, session))
            task.async_request = async_request
            task.add_done_callback(task_done_handler)
            tasks.append(task)

        return await asyncio.gather(*tasks, return_exceptions=True)


loop = asyncio.get_event_loop()
a = time()
async_requests = []
async_requests.append(AsyncRequest("https://docon.co.in", "get"))
async_requests.append(AsyncRequest("https://csdcsdcdcvdvsdocon.co.in", "get"))
future = asyncio.ensure_future(run(async_requests))
loop.run_until_complete(future)
print(time() - a)