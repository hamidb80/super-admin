from time import sleep
from typing import Dict


class E2ETestBase:
    outs = []

    @classmethod
    def setup_class(self):
        pass

    @property
    def new_outs(self) -> str:
        return ""

    def push_input(self, content):
        pass