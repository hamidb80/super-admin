from time import sleep
from threading import Thread
from connection import tunnel
from events import event_list
from connection_checker import connection_checker
from actions import command_input

# register events
for event in event_list:
    tunnel.on(event.name, event.function)

# start connection checker
Thread(target=connection_checker).start()

Thread(target=command_input).start()



# try to connect to the server at the first time
while True:
    try:
        tunnel.run()
    except:
        sleep(1)
