from time import sleep
from threading import Thread

from config import ADDR, PORT
from events import event_list
from tasks import task_list
from provider import states, services
from functions import get_host_name
from driver.core import Core
from driver.argumentparser import get_args
from driver.tunnel import Tunnel

if __name__ == "__main__":
    args = get_args()

    services.core = Core(
        debug_mode=args['test'],
        input_file_path=args['input_file'],
        output_file_path=args['output_file']
    )
    states.host_name = get_host_name()

    services.tunnel = Tunnel(ADDR, PORT)

    # register events
    for event in event_list:
        services.tunnel .on(event.name, event.func)

    # run background tasks
    for task in task_list:
        task.run()

    services.tunnel.run()
