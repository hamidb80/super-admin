from core import FileWatcher
from time import sleep

path = '../inp.txt'

file = FileWatcher(path, print)
file.run()

sleep(1)

print('stop')