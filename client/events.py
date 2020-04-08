from typing import List

from actions import connect, disconnect, auth, hello, reconnect
from driver.event import Event

from utils import events_names as ev

event_list: List[Event] = [
    # pre-defined events
    Event(ev.connect, connect),
    Event(ev.reconnect, reconnect),
    Event(ev.disconnect, disconnect),

    # user defined events
    Event(ev.hello, hello),
]
