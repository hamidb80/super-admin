from typing import Callable, List
import asyncio
from threading import Thread

from functions import connection_checker
from actions import main_input


class Task:
    def __init__(self, func: Callable):
        self.func = func

    def run(self):
        thread = Thread(target=self.func)
        thread.start()


task_list: List[Task] = [
    Task(main_input),
    Task(connection_checker)
]