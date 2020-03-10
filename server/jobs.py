from typing import Callable, List
from threading import Thread
from time import sleep

from functions import clean_messageDB


class Job:
    def __init__(self, func: Callable, repeat_after: int, start_delay: int = 0):
        self.func = func
        self.repeat_after = repeat_after
        self.start_delay = start_delay

    def run(self):
        Thread(target=self._go, daemon=True).start()

    def _go(self):
        sleep(self.start_delay)

        while True:
            self.func()
            sleep(self.repeat_after)


job_list: List[Job] = [
    Job(clean_messageDB, 10, 2)
]
