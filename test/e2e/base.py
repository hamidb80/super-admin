from subprocess import Popen, PIPE
from time import sleep
from typing import Dict
import os

from client.driver.core import FileWatcher, FileWriter
from config import OUT_FILE_PATH, INP_FILE_PATH


class E2ETestBase:
    @classmethod
    def setup_class(self):

        self.procs = dict(
            server=Popen(
                [f'python3.8 server/app.py -p=123'],
                shell=True,
                stdout=PIPE, stdin=PIPE, stderr=PIPE
            ),
            client=Popen(
                [f'python3.8 client/app.py -t --inpf="{INP_FILE_PATH}" --outf="{OUT_FILE_PATH}"'],
                shell=True,
                stdout=PIPE, stdin=PIPE, stderr=PIPE
            )
        )

        self.out_file = FileWatcher(OUT_FILE_PATH, lambda z: False)
        self.inp = FileWriter(INP_FILE_PATH)

    def test_connect(self):
        self.inp.append('status')

        sleep(0.6)
        out = self.out_file.get_content()

        assert 'not connected' not in out

    def test_send_hello(self):
        pass

    def teardown_class(self):
        # remove files after tests
        os.remove(INP_FILE_PATH)
        os.remove(OUT_FILE_PATH)

        app: Popen
        for app in self.procs.values():
            app.kill()