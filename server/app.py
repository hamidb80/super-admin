from config import ADDR, PORT


from events import event_list
from driver.tunnel import Tunnel
from tables import init_database
from provider import services

# make tunnel instance
tunnel = Tunnel(ADDR, PORT)
services.tunnel = tunnel


if __name__ == "__main__":

    # start database
    init_database()

    # register events
    for event in event_list:
        tunnel.on(event.name, event.func)

    # start tunnel
    tunnel.run()
