from typing import Callable, Any, Dict
from logging import Logger, INFO
from threading import Thread
from time import sleep

import requests

from provider import states, services
from .interface import TunnelIC
from config import UPDATE_DELAY


logger = Logger('Tunnel', level=INFO)


class Tunnel(TunnelIC):
    event_map: Dict[str, Callable] = dict()

    # {'event': <data>}
    queue_events: Dict[str, Any] = dict()

    def __init__(self, addr, port):
        self.address = f'http://{addr}:{port}'
        self.is_active = False

    # add event
    def on(self, event: str, func: Callable):
        logger.info(f'Event: {event}')
        self.event_map[event] = func

    def push_event(self, event: str, data: Any = None):
        # pass the queues
        if event in self.queue_events:
            self.queue_events[event] = data

        # run event functions
        func = self.event_map.get(event)

        if func:
            thread = Thread(target=lambda: func(data))
            thread.run()

        else:
            services.core.print(f'the {event} event is not defined')

    """
    return the data of the <event> after passing
    """
    def wait_for(self, event: str) -> Any:
        self.queue_events[event] = None

        while self.queue_events[event] is None:
            sleep(UPDATE_DELAY)

        data = self.queue_events[event]
        del self.queue_events[event]

        return data

    def send(self, event: str, data: Any = None):
        """
        POST /messages/{states.host_name}/
        data should be json like this:
        {
            'event': <event_name:str>,
            'data': <data_object:any>
        }
        """

        params = dict(
            event=event,
            data=data
        )

        return requests.post(f'{self.address}/commit/{states.host_name}', json=params)

    def get_messages(self):
        """
        GET /messages/{states.host_name}/
        the received data structure:
        {
            'messages':[
                {
                    'event': <event_name:str>
                    'data': <data_object:any>
                },
                ...
            ]
        }
        """

        try:
            res = requests.get(
                f'{self.address}/messages/{states.host_name}/', timeout=0.3)
        except:
            states.failed_to_connect()
            return

        else:
            states.connected_successfully()

        try:
            message_list = res.json()['messages']

        except:
            services.core.print('the response from server is not valid')
            return

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
            sleep(UPDATE_DELAY)
            self.get_messages()
