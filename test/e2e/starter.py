from subprocess import Popen, PIPE
from threading import Thread
from time import sleep


lines = []
live = True
proc: Popen = None


proc = Popen(['python3.8 ../../client/app.py'],
             stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)


def tracker():
    global lines, proc, live

    while live is True:
        lines.append(proc.stdout.readline())
        print(lines[-1])


Thread(target=tracker).start()

while True:
    sleep(0.1)
    proc.stdin.write(b'auth\n')

proc.kill()
live = False
