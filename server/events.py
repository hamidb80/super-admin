from typing import Callable, List

from functions import remove_from_offline_clients
from actions import (
    connect, reconnect, disconnect,
    executefromclient,auth
)


class Event:
    name: str
    function: Callable

    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func


event_list: List[Event] = [


    # pre-defined events
    Event('connect', remove_from_offline_clients),
    Event('connect', connect),
    Event('reconnect', reconnect),
    Event('disconnect', disconnect),

    # user defined events
    Event('execute', executefromclient),
    Event('auth', auth),
]
