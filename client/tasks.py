from typing import Callable, List
import asyncio
from threading import Thread

from functions import connection_checker
from actions import main_input


class Task:
    def __init__(self, func: Callable, is_async=False):
        self.func = func

    def run(self):
        thread = Thread(target=self.func, daemon=True)
        thread.start()


task_list: List[Task] = [
    Task(main_input),
    Task(connection_checker)
]