import eventlet
from socketio import Server, WSGIApp
from typing import Callable
import logging


default_logger = logging.getLogger('tunnel.logger')
default_logger.setLevel(logging.DEBUG)

class Tunnel:
    def __init__(self, addr, port):
        self.connection = (addr, port)

        self.socket = Server()

        self.app = WSGIApp(self.socket)

    def on(self, event: str, func: Callable):
        self.socket.on(event, handler=func)

    def send(self, event: str, data=None, socket_id=None):
        self.socket.emit(event, data=data, room=socket_id)

    def run(self):
        eventlet.wsgi.server(eventlet.listen(self.connection), self.app, log=default_logger)
