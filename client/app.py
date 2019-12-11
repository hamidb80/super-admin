from time import sleep
from threading import Thread

from connection import tunnel
from events import event_list
from connection_checker import connection_checker


# run in background
thread = Thread(target=connection_checker)
thread.start()

# register events
for event in event_list:
    tunnel.on(event.name, event.function)

# you can't add any event to tunnel after run this
while True:
    try:
        tunnel.run()
        break
    except:
        sleep(1)
