from server import tunnel
from actions import connect, newuser, disconnect, execute, givepass, has_access, denied_access
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
    Event('newuser', newuser),
    Event('execute', execute),
    Event('askforauth', givepass),
    Event('has_access', has_access),
    Event('denied_access', denied_access)
]