from typing import Callable, List

from functions import remove_from_offline_clients
from utils import event_names as ev
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
    Event(ev.connect, remove_from_offline_clients),
    Event(ev.connect, connect),
    Event(ev.reconnect, reconnect),
    Event(ev.disconnect, disconnect),

    # user defined events
    Event(ev.execute, execute_from_client),
    Event(ev.auth, auth),
]
