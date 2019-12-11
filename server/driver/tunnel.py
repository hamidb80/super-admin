import eventlet
from socketio import Server, WSGIApp
from typing import Callable


class Tunnel:
    def __init__(self, addr, port):
        self.connection = (addr, port)

        self.socket = Server()
        self.app = WSGIApp(self.socket)

    def on(self, event: str, func: Callable):
        self.socket.on(event, handler=func)

    def listen(self):
        eventlet.wsgi.server(eventlet.listen(self.connection), self.app)
