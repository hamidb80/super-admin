from time import sleep
from typing import Dict, Any
import os
from threading import Thread

from redis import Redis
from redis.client import PubSub

from client.config import UPDATE_DELAY

CLIENT_INPUT_CHANNEL = 'client-input'
CLIENT_OUTPUT_CHANNEL = 'client-output'


class E2ETestBase:
    outs = []
    isActive = True

    @classmethod
    def setup_class(self):
        self.init_testing()

    @classmethod
    def teardown_class(self):
        self.isActive = False

    @classmethod
    def init_testing(self):
        # redis server configuration
        redis_port = os.getenv('redis_port')

        self.redis_server = Redis('localhost', redis_port)

        self.pipeline = self.redis_server.pubsub()
        self.pipeline.subscribe(CLIENT_OUTPUT_CHANNEL)

        t = Thread(target=self.get_redis_messages)
        t.start()

    @classmethod
    def get_redis_messages(self):

        while self.isActive:
            ms = self.pipeline.get_message()

            if ms is None:
                continue

            if ms['type'] == 'message':
                # byte code to str (channel is byte-like str as default)
                ms_channel = ms['channel'].decode('utf-8')

                data = ms['data'].decode('utf-8')

                if ms_channel == CLIENT_OUTPUT_CHANNEL:
                    self.outs.append(data)

            sleep(UPDATE_DELAY)

    def get_outputs(self) -> str:
        outs = self.outs
        self.outs = []

        return ''.join(outs)

    def push_input(self, text: str):
        self.redis_server.publish(CLIENT_INPUT_CHANNEL, text)
