from typing import Callable, List
from actions import connect, disconnect, auth, hello



class Event:
    name: str
    function: Callable

    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func


event_list: List[Event] = [
    Event('connect', connect),
    Event('hello', hello),
    Event('disconnect', disconnect),
    Event('auth', auth),
]
