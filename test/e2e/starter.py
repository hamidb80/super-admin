from subprocess import Popen
from threading import Thread
from time import sleep
import os

from core import FileWriter, FileWatcher

proc: Popen = None
outs = []
os.chdir('../../')


def tracker():
    global proc

    proc = Popen(
        ['python3.8 client/app.py -t --inpf="test/inp.txt" --outf="test/out.txt"'], shell=True)

    proc.wait()
    # proc.kill()


def add_to_outs(content):
    global outs

    outs.append(content)

    return True


def main():
    Thread(target=tracker).start()

    sleep(0.2)
    print('1')
    out = FileWatcher('test/out.txt', add_to_outs)
    out.run()

    print('2')
    sleep(0.1)
    inp = FileWriter('test/inp.txt')
    inp.clear()

    print('3')
    sleep(0.1)
    inp.append('status')

    print('4')
    sleep(0.1)
    print(outs)

if __name__ == "__main__":
    main()