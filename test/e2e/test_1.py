from subprocess import Popen, PIPE
from threading import Thread
from time import sleep
from typing import Dict
import os

from core import FileWriter, FileWatcher

procs: Dict[str, Popen] = dict(
    client=None,
    server=None,
)

outs = []
os.chdir('../../')

INP_FILE_PATH = 'test/inp.txt'
OUT_FILE_PATH = 'test/out.txt'


def start_app():
    global proc

    procs['server'] = Popen(
        [f'python3.8 server/app.py -p=123'],
        shell=True,
        stdout=PIPE, stdin=PIPE, stderr=PIPE
    )

    procs['client'] = Popen(
        [f'python3.8 client/app.py -t --inpf="{INP_FILE_PATH}" --outf="{OUT_FILE_PATH}"'],
        shell=True,
        stdout=PIPE, stdin=PIPE, stderr=PIPE
    )


def close_app():
    app: Popen
    for app in procs.values():
        app.kill()


def main():
    out_file = FileWatcher(OUT_FILE_PATH, lambda z: False)
    inp = FileWriter(INP_FILE_PATH)

    start_app()

    sleep(0.5)
    inp.append('status')

    sleep(1)
    out = out_file.get_content()

    assert 'not connected' not in out

    close_app()


if __name__ == "__main__":
    main()
