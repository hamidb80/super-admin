from typing import List

from actions import connect, disconnect, auth, hello, reconnect
from .event import Event, events_names as ev

event_list: List[Event] = [
    # pre-defined events
    Event(ev.connect.value, connect),
    Event(ev.reconnect.value, reconnect),
    Event(ev.disconnect.value, disconnect),

    # user defined events
    Event(ev.hello.value, hello),
]
