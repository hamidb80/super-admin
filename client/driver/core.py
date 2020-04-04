from typing import Any, Callable
from enum import Enum
from threading import Thread
import os

# TODO: do debug mode with Redis

class os_list(Enum):
    linux = 'linux'
    windows = 'win'


class Core:
    def __init__(self, debug_mode: bool):
        self.debug_mode = debug_mode
        self.os = 'linux'

        self.res = ''

        if debug_mode:
            pass

    def pass_into_res(self, file, content) -> bool:
        self.res = content
        # to stop
        return False

    def print(self, content: Any):
        content = f'{content}\n'

        if self.debug_mode:
            pass

        else:
            return print(content)

    def input(self, text: str):
        if self.debug_mode:

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
