from typing import Callable, List
from actions import connect, disconnect, auth, hello, reconnect


class Event:
    """
    event class just for increase readability
    """

    name: str
    function: Callable

    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func


event_list: List[Event] = [
    # pre-defined events
    Event('connect', connect),
    Event('reconnect', reconnect),
    Event('disconnect', disconnect),

    # user defined events
    Event('hello', hello),
    Event('auth', auth),
]
