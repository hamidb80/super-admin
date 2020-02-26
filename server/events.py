from typing import Callable, List

from actions import connect, executefromclient, notification



class Event:
    name: str
    function: Callable

    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func


event_list: List[Event] = [
    Event('connect', connect),
    Event('notification', notification),
    Event('execute', executefromclient),
]
