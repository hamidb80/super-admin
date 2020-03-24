from typing import Callable, List, Dict, Any
import logging

from collections import defaultdict

from flask import Flask, request, Response

from .models import Client, Message
from .views import commit_view, messages_view
from provider import services
from jobs import Job


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class Tunnel:
    event_map: Dict[str, List[Callable]]

    def __init__(self, addr, port):
        self.event_map = defaultdict(list)

        self.connection = (addr, port)
        self.app = Flask('tunnel')

    def on(self, event: str, func: Callable):
        # func (client:Client): ...
        self.event_map[event].append(func)

    def push_event(self, event: str, client: Client, data: Any = None):
        for func in self.event_map[event]:
            func(client, data)

    def send(self, event: str, target: str, data: Any):
        new_msg = Message(target=target, event=event, data=data)
        new_msg.save()

    def init_routes(self):
        # self.app.add_url_rule('/messages/',
        self.app.add_url_rule('/messages/<host_name>/',
                              methods=['GET'],
                              view_func=messages_view)

        self.app.add_url_rule('/commit/<host_name>',
                              methods=["POST"],
                              view_func=commit_view)

    def run(self):
        self.init_routes()
        self.app.run(host=self.connection[0],
                     port=self.connection[1], debug=False)
