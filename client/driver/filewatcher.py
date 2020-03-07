from typing import Callable
from threading import Thread


class FileWatcher:
    def __init__(self, file_path: str, action_func: Callable):
        self.is_active = False

        self.action_func = action_func
        self.file_path = file_path

    def kill(self):
        self.is_active = False

    def run(self, action: Callable, wait=False):
        self.is_active = True

        if wait is False:

            thread = Thread(target=self._go)
            thread.run()

        else:
            self._go()

    def get_content(self) -> str:
        with open(self.file_path) as file:
            return file.read()

    def _go(self):
        last_content = self.get_content()

        while self.is_active:
            content = self.get_content()

            if content != last_content:

                last_content = content
                res = self.action_func(content)

                if res is False:
                    self.kill()
