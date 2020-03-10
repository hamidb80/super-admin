from subprocess import Popen, PIPE
from threading import Thread
from time import sleep
import os

from core import FileWriter, FileWatcher

proc: Popen = None
outs = []
os.chdir('../../')

INP_FILE_PATH = 'test/inp.txt'
OUT_FILE_PATH = 'test/out.txt'


def tracker():
    global proc

    proc = Popen(
        [f'python3.8 client/app.py -t --inpf="{INP_FILE_PATH}" --outf="{OUT_FILE_PATH}"'],
        shell=True,
         stdout=PIPE, stdin=PIPE, stderr=PIPE
    )

    proc.wait()
    # proc.kill()


def main():
    Thread(target=tracker).start()

    sleep(0.2)
    print('1')
    out_file = FileWatcher(OUT_FILE_PATH, lambda z: False)

    print('2')
    sleep(0.1)
    inp = FileWriter(INP_FILE_PATH)

    print('3')
    sleep(0.1)
    inp.append('status')

    print('4')
    sleep(1)
    out = out_file.get_content()

    assert 'not connected' in out

    proc.kill()


if __name__ == "__main__":
    main()
