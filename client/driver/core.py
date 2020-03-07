from typing import Any
from enum import Enum
import os

from .filewatcher import FileWatcher


class os_list(Enum):
    linux = 'linux'
    windows = 'win'


class Core:
    def __init__(self, debug_mode: bool, print_file_path: str = '', input_file_path: str = ''):
        self.debug_mode = debug_mode
        self.os = 'linux'

        self.input_file_path = input_file_path
        self.print_file_path = print_file_path

    def print(self, content: Any):
        content = str(content)

        if self.debug_mode:
            with open(self.print_file_path, 'w+') as file:
                file.write(content)

        else:
            return print(content)

    def input(self, text: str):
        res = None

        if self.debug_mode:

            inp_file: FileWatcher

            def pass_into_res(content) -> bool:
                global res, inp_file
                res = content

                # to stop
                return False

            inp_file = FileWatcher(self.input_file_path, pass_into_res)
            inp_file.run(pass_into_res, wait=True)

            return res

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
