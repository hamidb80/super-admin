from abc import ABC, abstractmethod
from socketio import Server
from typing import Callable

class TunnelIC:
    socket: Server

    @abstractmethod
    def __init__(self, addr: str, port: int):
        pass

    @abstractmethod
    def on(self, event: str, func: Callable):
        pass

    @abstractmethod
    def send(self, event: str, data=None, socket_id=None):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass
