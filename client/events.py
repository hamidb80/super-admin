from connection import tunnel
from actions import connect, disconnect , auth
from typing import Callable, List


class Event:
    name: str
    function: Callable

    def __init__(self, name: str, func: Callable):
        self.name = name
        self.function = func


event_list: List[Event] = [
    Event('connect', connect),
    Event('disconnect', disconnect),
    Event('auth', auth)
]
