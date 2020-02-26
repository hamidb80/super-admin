from typing import Callable, Any, Dict
import requests
from threading import Thread
from time import sleep
from provider import states, services

from .interface import TunnelIC


class Tunnel(TunnelIC):
    event_map: Dict[str, Callable] = dict()
    delay = 0.1

    def __init__(self, addr, port):
        self.address = f'http://{addr}:{port}'
        self.is_active = False

    # add event
    def on(self, event: str, func: Callable):
        self.event_map[event] = func

    def push_event(self, event: str, data: Any = None):
        func = self.event_map.get(event)

        if func:
            thread = Thread(target=lambda: func(data))
            thread.run()

        else:
            services.core.print(f'the {event} event is not defined')

    def send(self, event: str, data: Any = None):
        params = dict(
            event=event,
            data=data
        )

        # TODO: change it to POST request
        return requests.get(f'{self.address}/commit/', params=params)

    def get_messages(self):
        try:
            res = requests.get(
                f'{self.address}/messages/{states.host_name}/', timeout=0.3)
        except:
            states.failed_to_connect()
            return

        else:
            states.connected_successfully()

        message_list = res.json()['messages']

        for message in message_list:
            self.push_event(message['event'], message['data'])

    def disconnect(self):
        self.is_active = False

    def run(self):
        self.is_active = True

        thread = Thread(target=self._go)
        thread.run()

    def _go(self):
        while self.is_active:
            sleep(self.delay)
            self.get_messages()
