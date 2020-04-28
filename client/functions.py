from time import sleep
from socket import gethostname

from config import ADDR
from provider import states, services

from monkey_patch import print
from utils import Messages


def get_host_name():
    # get hostname
    return gethostname()


def lock():
    services.core.lock()


def common_commands(command: str):
    if '' == command:
        pass

    elif 'clear' == command:
        services.core.clear_console()

    else:
        print(Messages.command_not_defined)
