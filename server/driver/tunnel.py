from typing import Callable, List, Dict, Any
from collections import defaultdict
import logging

from flask import Flask, request, Response

from .models import Client, Message
from .views import commit_view, messages_view
from jobs import Job
from utils import event_names as ev


class Tunnel:
    logger = logging.getLogger('tunnel')
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
            try:
                func(client, data)
            except Exception as e:
                self.logger.error(f"error running event {event}")
                self.logger.error(e)

    def send(self, event: str, target: str, data: Any):
        new_msg = Message(target=target, event=event, data=data)
        new_msg.save()

    def init_routes(self):
        self.app.add_url_rule('/messages/<host_name>/',
                              methods=['GET'],
                              view_func=messages_view)

        self.app.add_url_rule('/commit/<host_name>',
                              methods=["POST"],
                              view_func=commit_view)

    def run(self):
        # config flask logger
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        self.init_routes()
        self.app.run(host=self.connection[0],
                     port=self.connection[1], debug=False)
