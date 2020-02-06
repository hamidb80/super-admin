from typing import Callable, List
import asyncio
from threading import Thread

from connection_checker import connection_checker
from actions import main_input


class Task:
    def __init__(self, func: Callable, is_async=False):
        self.func = func
        self.is_async = is_async

    def run(self, loop: asyncio.BaseEventLoop = None):
        thread: Thread

        loop = asyncio.new_event_loop()

        if self.is_async:
            def action():
                loop.run_until_complete(self.func())

            thread = Thread(target=action)

        else:
            thread = Thread(target=self.func)

        thread.start()


task_list: List[Task] = [
    Task(main_input, True),
    Task(connection_checker)
]
