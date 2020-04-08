from typing import Any, Callable
from threading import Thread
import os

# TODO: do debug mode with Redis

class os_list:
    linux = 'linux'
    windows = 'win'


class Core:
    def __init__(self, test_mode: bool):
        self.test_mode = test_mode

        # FIXME: get os name from os module
        self.os = os_list.linux

        if test_mode:
            self.init_testing()

    def init_testing(self):
        # TODO: connect to redis server ...
        redis_port = os.getenv('redis_port')

    def print(self, content: Any):
        content = f'{content}\n'

        if self.test_mode:
            pass

        else:
            return print(content)

    def input(self, text: str):
        if self.test_mode:

            self.print(text)

            # self.input_obj.run(self.pass_into_res, wait=True)
            return ''

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

