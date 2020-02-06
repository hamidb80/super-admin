from time import sleep
import asyncio
from threading import Thread

from connection import tunnel
from events import event_list
from tasks import task_list


if __name__ == "__main__":

    # register events
    for event in event_list:
        tunnel.on(event.name, event.func)

    for task in task_list:
        task.run()

    # try to connect to the server
    while True:
        try:
            tunnel.run()
            break
        except:
            sleep(1)
