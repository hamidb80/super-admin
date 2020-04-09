from typing import Any, Callable, Dict
from threading import Thread
from time import sleep
import os

from redis import Redis
from redis.client import PubSub

from config import UPDATE_DELAY


class os_list:
    linux = 'linux'
    windows = 'win'


CLIENT_INPUT_CHANNEL = 'client-input'
CLIENT_OUTPUT_CHANNEL = 'client-output'


class Core:
    redis_server: Redis
    pipeline: PubSub

    ms_queue: Dict[str, Any] = dict()

    def __init__(self, test_mode: bool):
        self.test_mode = test_mode

        # FIXME: get os name from os module
        self.os = os_list.linux

        if test_mode:
            self.init_testing()

    def init_testing(self):
        # redis server configuration
        redis_port = os.getenv('redis_port')

        self.redis_server = Redis('127.0.0.1', redis_port)

        self.pipeline = self.redis_server.pubsub()
        self.pipeline.subscribe(CLIENT_INPUT_CHANNEL)

    def get_redis_messages(self):
        while True:
            ms = self.pipeline.get_message()

            if ms['type'] == 'message':
                # byte code to str (channel is byte-like str as default)
                ms_channel = ms['channel'].decode('utf-8')

                if ms_channel in self.ms_queue:
                    self.ms_queue[ms_channel] = ms['data']

            sleep(UPDATE_DELAY)

    def wait_for_redis_channel(self, channel_name: str, time_limit: float = 0):
        spent_time = 0

        while channel_name not in self.ms_queue:
            if time_limit and spent_time >= time_limit:
                raise TimeoutError

            sleep(UPDATE_DELAY)
            spent_time += UPDATE_DELAY

        return self.ms_queue[channel_name]

    def print(self, content: Any):
        content = f'{content}\n'

        if self.test_mode:
            self.redis_server.publish(CLIENT_OUTPUT_CHANNEL, content)

        else:
            return print(content)

    def input(self, text: str):
        if self.test_mode:
            self.print(text)

            return self.wait_for_redis_channel(CLIENT_INPUT_CHANNEL)

        else:
            return input(text)

    # windows, linux
    def clear_console(self):
        command = None
        if self.os is os_list.linux:
            command = 'clear'

        elif self.os is os_list.windows:
            command = 'cls'

        os.system(command)

    def lock(self):
        if self.test_mode:
            self.print('locked')

        else:
            #os.system('rundll32.exe user32.dll,LockWorkStation')
            pass
