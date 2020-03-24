from typing import Callable, List
from threading import Thread
from time import sleep

from functions import clean_messageDB, check_for_disconnection


class Job:
    """
    in computer science, job is a task that runs after certain time
    for more than 1 time
    """
    def __init__(self, func: Callable, repeat_after: int, start_delay: int = 0):
        self.func = func
        self.repeat_after = repeat_after
        self.start_delay = start_delay

    def run(self):
        Thread(target=self._go).start()

    def _go(self):
        sleep(self.start_delay)

        while True:
            self.func()
            sleep(self.repeat_after)


job_list: List[Job] = [
    Job(clean_messageDB, 10, 2),
    Job(self.check_for_disconnection, 1, 1)
]