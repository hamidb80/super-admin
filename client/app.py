from time import sleep
from threading import Thread
from connection import tunnel
from events import event_list
from connection_checker import connection_checker
from actions import main_input

if __name__ == "__main__":
    
    # register events
    for event in event_list:
        tunnel.on(event.name, event.function)

    # start connection checker
    Thread(target=connection_checker).start()

    # start main input
    Thread(target=main_input).start()



    # try to connect to the server
    while True:
        try:
            tunnel.run()
        except:
            sleep(1)
