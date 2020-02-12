from typing import Callable, List

from connection import tunnel
from actions import connect, disconnect, auth, ischecked



class Event:
    name: str
    function: Callable

    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func


event_list: List[Event] = [
    Event('connect', connect),
    Event('disconnect', disconnect),
    Event('auth', auth),
    Event('checked',ischecked)
]
