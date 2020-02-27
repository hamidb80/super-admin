from typing import Callable, List, Dict, Any

from .models import Client, Message
from .views import commit_view, messages_view
from provider import services

from flask import Flask, request, Response


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class Tunnel:
    event_map: Dict[str, Callable]

    def __init__(self, addr, port):
        self.event_map = dict()

        self.connection = (addr, port)
        self.app = Flask('tunnel')

    def on(self, event: str, func: Callable):
        # func (client:Client): ...
        self.event_map[event] = func

    def push_event(self, event: str, client: Client, data: Any= None):
        return self.event_map[event](client, data)

    def send(self, event: str, target: str, data: Any):
        new_msg = Message(target, event, data)
        new_msg.save()

    def init_routes(self):
        # self.app.add_url_rule('/messages/',
        self.app.add_url_rule('/messages/<host_name>/',
                              methods=['GET'],
                              view_func=messages_view)

        self.app.add_url_rule('/commit/',
                              methods=["POST", "GET"],
                              view_func=commit_view)

    def run(self):
        self.init_routes()
        self.app.run(host=self.connection[0],
                     port=self.connection[1], debug=False)
