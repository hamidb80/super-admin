from time import sleep
from threading import Thread
from config import tunnel
from events import event_list
from connection_checker import connection_checker

cn = Thread(target=connection_checker)

# Register events
for event in event_list:
    tunnel.on(event.name, event.function)

if __name__ == "__main__":
    cn.start()

    # try to connect to the server at the first time
    while True:
        try:
            tunnel.run()
        except:
            sleep(1)
