from aiohttp import web
from socketio import AsyncServer
from typing import Callable
import logging

from .models import Client
from provider import services

class Tunnel:
    def __init__(self, addr, port):
        self.connection = (addr, port)
        self.socket = AsyncServer(async_mode='aiohttp')
        self.app = web.Application()

        self.socket.attach(self.app)

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
        web.run_app(self.app, host=self.connection[0], port=self.connection[1])

    def disconnect(self):
        self.app.shutdown()
