from subprocess import Popen, PIPE
from time import sleep
from typing import Dict
import os

from client.driver.core import FileWatcher, File
from config import OUT_FILE_PATH, INP_FILE_PATH


class E2ETestBase:
    outs = []

    @classmethod
    def setup_class(self):
        # setup input/output files
        File(OUT_FILE_PATH).append('')
        self.out_file = FileWatcher(OUT_FILE_PATH)
        self.inp = File(INP_FILE_PATH)

    @property
    def new_outs(self) -> str:
        outs = self.out_file.get_content()
        self.outs.append(outs)
        self.clear_output()

        return outs

    def push_input(self, content):
        self.inp.append(content)

    def clear_output(self):
        self.out_file.clear()
