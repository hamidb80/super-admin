from time import sleep
from threading import Thread

from config import ADDR, PORT
from events import event_list
from tasks import task_list
from provider import states
from functions import get_host_name
from driver.core import Core
from driver.tunnel import Tunnel


if __name__ == "__main__":

    states.core = Core(debug_mode=False)

    states.tunnel = Tunnel(ADDR, PORT)
    states.host_name = get_host_name()

    # register events
    for event in event_list:
        states.tunnel .on(event.name, event.func)

    # run background tasks
    for task in task_list:
        task.run()

    states.tunnel.run()
