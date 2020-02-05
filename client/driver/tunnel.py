from socketio import AsyncClient
from typing import Callable, Any
import asyncio
import time


class Tunnel:
    def __init__(self, addr, port):
        self.address = (addr, port)

        self.socket = AsyncClient()
        self.loop = asyncio.get_event_loop()

    # add event
    def on(self, event: str, func: Callable):
        self.socket.on(event, func)

    async def send(self, event: str, data: Any = None):
        await self.socket.emit(event, data=data)

    async def disconnect(self):
        await self.socket.disconnect()

    def run(self):
        self.loop.run_until_complete(self._start())

    async def _start(self):
        await self.socket.connect(f'http://{self.address[0]}:{self.address[1]}')
        await self.socket.wait()
