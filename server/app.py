from driver.models import Client, Message
from driver.tunnel import Tunnel
from driver.argumentparser import get_args
from typing import Any, List

from config import ADDR, PORT

from events import event_list
from database import init_database
from provider import services
from utils import set_serverpass

from provider import services
from jobs import job_list


tunnel = Tunnel(ADDR, PORT)
services.tunnel = tunnel


def main():
    # set server's password
    args = get_args()

    password = args['password']
    set_serverpass(password)


    # start database
    init_database()

    # register events
    for event in event_list:
        tunnel.on(event.name, event.func)

    for job in job_list:
        job.run()

    # start server
    tunnel.run()


if __name__ == "__main__":
    main()
