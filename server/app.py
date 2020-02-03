from config import ADDR, PORT

from states import services
from events import event_list
from driver.tunnel import Tunnel
from tables import init_databases

# make tunnel instance
tunnel = Tunnel(ADDR, PORT)
services.tunnel = tunnel



if __name__ == "__main__":
    
    # register events
    for event in event_list:
        tunnel.on(event.name, event.func)

    # start database
    init_databases()
    
    # start tunnel
    tunnel.run()
