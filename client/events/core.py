from typing import Callable
from enum import Enum

class Event:
    """
    event class just for increase readability
    """

    name: str
    function: Callable

    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func


class events_names(Enum):
    connect = 'connect'
    reconnect = 'reconnect'
    disconnect = 'disconnect'

    hello = 'hello'
    auth = 'auth'

    auth_check = 'auth_check'