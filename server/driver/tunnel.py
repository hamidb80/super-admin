import eventlet
from socketio import Server, WSGIApp
from typing import Callable

import logging
default_logger = logging.getLogger('tunnel.logger')
# default_logger.setLevel(logging.CRITICAL)
# default_logger.disabled = True

class Tunnel:
    def __init__(self, addr, port):
        self.connection = (addr, port)

        self.socket = Server(logger=default_logger,
                             engineio_logger=default_logger)

        print(default_logger)
        self.app = WSGIApp(self.socket)

    def on(self, event: str, func: Callable):
        self.socket.on(event, handler=func)

    def send(self, event: str, data=None, socket_id=None):
        self.socket.emit(event, data=data, room=socket_id)

    def listen(self):
        eventlet.wsgi.server(eventlet.listen(self.connection), self.app)
