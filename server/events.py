from server import tunnel
from actions import connect, newname, disconnect, execute
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
    Event('newname', newname),
    Event('execute', execute)
]
