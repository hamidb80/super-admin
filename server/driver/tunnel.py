import eventlet
from socketio import Server, WSGIApp
from typing import Callable
import logging

from .models import Client
from provider import services

default_logger = logging.getLogger('tunnel.logger')
default_logger.setLevel(logging.DEBUG)


class Tunnel:
    def __init__(self, addr, port):
        self.connection = (addr, port)
        self.socket = Server()
        self.app = WSGIApp(self.socket)

    def on(self, event: str, func: Callable):

        def wrapper(socket_id, *args, **kwargs):

            client = services.clientDB.find(socket_id=socket_id)
            if client is None:
                client = Client(socket_id)

            return func(client, *args, **kwargs)

        self.socket.on(event, handler=wrapper)

    def send(self, event: str, data=None, socket_id=None):
        self.socket.emit(event, data=data, room=socket_id)

    def run(self):
        print(
            f'tunnel is running on {self.connection[0]}:{self.connection[1]}'
        )

        eventlet.wsgi.server(eventlet.listen(
            self.connection), self.app, log = default_logger)

    def disconnect(self):
        pass
