from socketio import Client
from typing import Callable, Any


class Tunnel:
    def __init__(self, addr, port):
        self.socket = Client()
        self.address = (addr, port)

    # add event
    def on(self, event: str, func: Callable):
        self.socket.on(event, func)

    def send(self, event: str, data: Any = None):
        self.socket.emit(event, data=data)

    def run(self):
        self.socket.connect(f'http://{self.address[0]}:{self.address[1]}')
        self.socket.wait()

    def stop(self):
        self.socket.disconnect()
