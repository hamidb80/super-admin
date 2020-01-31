from states import services
from events import event_list
from driver.tunnel import Tunnel
from tables import init_databases

from config import ADDR, PORT


tunnel = Tunnel(ADDR, PORT)
services.tunnel = tunnel

init_databases()

# register events
for event in event_list:
    tunnel.on(event.name, event.function)

if __name__ == "__main__":
    tunnel.run()
