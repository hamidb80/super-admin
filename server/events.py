from typing import Callable, List

from functions import remove_from_offline_clients
from utils import event_names as ev
from actions import (
    connect, reconnect, disconnect,
    execute_from_client, auth, online_users,
    send_event
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
    Event(ev.auth, auth),
    Event(ev.send_event, send_event),
    Event(ev.execute, execute_from_client),
    Event(ev.online_users, online_users),
]
