from enum import Enum
import os


class os_list(Enum):
    linux = 'linux'
    windows = 'win'


class Core:
    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode
        self.os = os_list.linux

    def print(self, *args, **kwargs):

        if self.debug_mode:
            pass

        else:
            return print(*args, **kwargs)

    def input(self, text: str):
        if self.debug_mode:
            pass

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
