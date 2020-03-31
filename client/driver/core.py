from typing import Any, Callable
from enum import Enum
from threading import Thread
import os


class File:
    file_path: str

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.clear()

    def clear(self):
        with open(self.file_path, 'w') as file:
            file.truncate(0)

    def get_content(self) -> str:
        with open(self.file_path) as file:
            return file.read()

    def append(self, content):
        last_content = self.get_content()

        with open(self.file_path, 'w+') as file:
            file.write(f'{last_content}{content}')


class FileWatcher(File):
    """
    sample action file

    def action(file:File, content) -> continue_watching? : bool:
        return True
    """

    def __init__(self, file_path: str):
        super().__init__(file_path)

        self.is_active = False

    def kill(self):
        self.is_active = False

    def run(self, action_func=lambda *_: True, wait=False):
        self.is_active = True

        if wait:
            self._go(action_func)

        else:
            thread = Thread(target=self._go, args=[action_func])
            thread.start()

    def _go(self, action_func: Callable):
        last_content = self.get_content()

        while self.is_active:
            content = self.get_content()

            if content != last_content:

                last_content = content
                res = action_func(self, content)

                if res is not True:
                    self.kill()


class os_list(Enum):
    linux = 'linux'
    windows = 'win'


class Core:
    def __init__(self, debug_mode: bool, output_file_path: str = '', input_file_path: str = ''):
        self.debug_mode = debug_mode
        self.os = 'linux'

        self.res = ''

        if debug_mode:
            self.input_obj = FileWatcher(input_file_path)
            self.print_obj = File(output_file_path)

            self.input_obj.clear()
            self.print_obj.clear()

    def pass_into_res(self, file, content) -> bool:
        self.res = content
        # to stop
        return False

    def print(self, content: Any):
        content = f'{content}\n'

        if self.debug_mode:
            self.print_obj.append(content)

        else:
            return print(content)

    def input(self, text: str):
        if self.debug_mode:

            self.print(text)

            self.input_obj.run(self.pass_into_res, wait=True)

            res = self.res
            self.res = ''

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
