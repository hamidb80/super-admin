from time import sleep
from threading import Thread

from connection import tunnel
from events import event_list
from actions import main_input
from tasks import task_list
from states import app_state
from driver.core import Core

if __name__ == "__main__":

    app_state.core = Core(debug_mode=False)

    # register events
    for event in event_list:
        tunnel.on(event.name, event.func)

    # run background tasks
    for task in task_list:
        task.run()

    # try to connect to the server at the first time
    while True:
        try:
            tunnel.run()
        except:
            sleep(1)
