from driver.models import Client, Message
from driver.tunnel import Tunnel
from typing import Any, List

from config import ADDR, PORT

from events import event_list
from database import init_database
from provider import services
from utils import set_serverpass

from provider import services


tunnel = Tunnel(ADDR, PORT)
services.tunnel = tunnel
if __name__ == "__main__":

    # set server's password
    # set_serverpass()

    # start database
    init_database()

    # register events
    for event in event_list:
        tunnel.on(event.name, event.func)

    # start server
    tunnel.run()
