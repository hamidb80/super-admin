from time import sleep
from socket import gethostname

from config import ADDR
from provider import states, services

def get_host_name():
    # get hostname
    return gethostname()

def lock():
    services.core.lock()
