from typing import List

from driver.event import Event
from utils.statics import events_names as ev

from actions import (
    connect, disconnect, reconnect,
    hello
)

event_list: List[Event] = [
    # pre-defined events
    Event(ev.connect, connect),
    Event(ev.reconnect, reconnect),
    Event(ev.disconnect, disconnect),

    Event(ev.hello, hello)
]
