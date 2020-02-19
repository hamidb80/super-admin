from typing import Callable, List, Dict

from .models import Client, Message
from .views import login_view, commit_view, messages_view
from provider import services

from flask import Flask, request, Response


class Tunnel:
    event_map: Dict[str, Callable]

    def __init__(self, addr, port):
        self.connection = (addr, port)
        self.app = Flask('tunnel')
        self.event_map = dict()

    def on(self, event: str, func: Callable):
        # func (client:Client): ...
        self.event_map[event] = func

    def push_event(self, event: str, client_name: str):
        client = services.clientDB.exists(host_name=client_name)

        if client is None:
            client = Client(client_name)

        return self.event_map[event](client)

    def send(self, message: Message):
        services.messageDB.add(Message)

    def init_routes(self):
        # self.app.add_url_rule('/messages/',
        self.app.add_url_rule('/messages/<host_name>/',
                              methods=['GET'],
                              view_func=messages_view)

        self.app.add_url_rule('/commit/',
                              methods=["POST", "GET"],
                              view_func=commit_view)

        self.app.add_url_rule('/login/',
                              methods=["POST", "GET"],
                              view_func=login_view)

    def run(self):
        self.init_routes()
        self.app.run(host=self.connection[0], port=self.connection[1], debug=True)
