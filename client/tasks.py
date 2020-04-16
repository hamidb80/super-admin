from typing import Callable, List
from threading import Thread

from actions import client_input


class Task:
    def __init__(self, func: Callable):
        self.func = func

    def run(self):
        thread = Thread(target=self.func)
        thread.start()


task_list: List[Task] = [
    Task(client_input),
]