from time import sleep
from threading import Thread

from config import ADDR, PORT

from events import event_list
from tasks import task_list

from provider import states, services
from driver.core import Core
from driver.argumentparser import get_args
from driver.tunnel import Tunnel

from functions import get_host_name

if __name__ == "__main__":
    args = get_args()

    services.core = Core(
        # test_mode=args['test'],
        test_mode=True,
    )
    states.host_name = get_host_name()

    services.tunnel = Tunnel(ADDR, PORT)

    # register events
    for event in event_list:
        services.tunnel.on(event.name, event.func)

    # run background tasks
    for task in task_list:
        task.run()

    services.tunnel.run()
