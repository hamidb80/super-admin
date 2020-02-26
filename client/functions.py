from time import sleep

from config import ADDR
from provider import states
from actions import lock

from socket import gethostname

def get_host_name():
    # get hostname
    return gethostname()