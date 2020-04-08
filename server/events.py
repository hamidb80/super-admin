from typing import Callable, List

from functions import remove_from_offline_clients
from actions import (
    connect, reconnect, disconnect,
    execute_from_client, auth
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
    Event('execute', execute_from_client),
    Event('auth', auth),
]
