from subprocess import Popen, PIPE
from time import sleep
from typing import Dict
import os

from client.driver.core import FileWatcher, FileWriter
from config import OUT_FILE_PATH, INP_FILE_PATH


class E2ETestBase:
    outs = []

    @classmethod
    def setup_class(self):

        # start processes
        self.procs = dict(
            server=Popen(
                [f'python3.8 server/app.py -p=123'],
                shell=True,
                stdout=PIPE, stdin=PIPE, stderr=PIPE
            ),
            client=Popen(
                [f'python3.8 client/app.py -t --inpf="{INP_FILE_PATH}" --outf="{OUT_FILE_PATH}"'],
                shell=True,
                # stdout=PIPE, stdin=PIPE, stderr=PIPE
            )
        )

        # setup input/output files
        FileWriter(OUT_FILE_PATH).append('')
        self.out_file = FileWatcher(OUT_FILE_PATH, lambda *_: True)
        self.inp = FileWriter(INP_FILE_PATH)

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

    def teardown_class(self):
        # remove files after tests
        os.remove(INP_FILE_PATH)
        os.remove(OUT_FILE_PATH)

        # kill processes
        app: Popen
        for app in self.procs.values():
            app.kill()
