from typing import Any, Callable, Dict
from threading import Thread
from time import sleep
import os
import sys

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

        self.os = self.detect_os()

        if test_mode:
            self.init_testing()

    def detect_os(self) -> str:
        os_name = sys.platform

        if os_list.linux in os_name:
            return os_list.linux

        elif os_list.windows in os_name:
            return os_list.linux

        else:
            raise Exception("The os is not supported")

    def init_testing(self):
        # redis server configuration
        redis_port = os.getenv('redis_port')

        self.redis_server = Redis('127.0.0.1', redis_port)

        self.pipeline = self.redis_server.pubsub()
        self.pipeline.subscribe(CLIENT_INPUT_CHANNEL)

        # redis message queue thread
        thread = Thread(target=self.get_redis_messages)
        thread.start()

    def get_redis_messages(self):
        while True:
            # message as ms
            ms = self.pipeline.get_message()

            if ms is None:
                continue

            """
            redis message: {
                'type': str,
                'channel: byte-str,
                'data': byte-str,
            }
            """
            if ms['type'] == 'message':
                # byte code to str (channel & data is byte-like str as default)
                ms_channel = ms['channel'].decode('utf-8')
                ms_data = ms['data'].decode('utf-8')

                if ms_channel in self.ms_queue:
                    self.ms_queue[ms_channel] = ms_data

            sleep(UPDATE_DELAY)

    def wait_for_redis_channel(self, channel_name: str, time_limit: float = 0):
        spent_time = 0

        self.ms_queue[channel_name] = None

        while self.ms_queue[channel_name] is None:
            if time_limit and spent_time >= time_limit:
                raise TimeoutError

            sleep(UPDATE_DELAY)
            spent_time += UPDATE_DELAY

        res = self.ms_queue[channel_name]
        del self.ms_queue[channel_name]

        return res

    def print(self, content: Any):
        content = f'{content}\n'

        if self.test_mode:
            self.redis_server.publish(CLIENT_OUTPUT_CHANNEL, content)

        else:
            return print(content)

    def input(self, text: str):
        if self.test_mode:
            self.print(text)

            res = self.wait_for_redis_channel(CLIENT_INPUT_CHANNEL)
            return res

        else:
            return input(text)

    # windows, linux
    def clear_console(self):
        if self.test_mode:
            self.print('the screen cleared')
            return

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
