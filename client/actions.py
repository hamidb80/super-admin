from config import tunnel
from threading import Thread
from states import app_state
import socket

# Defining command input


def command_input():
    while True:
        inp = input('> ')
        try:
            print(f"I got it -{inp}")
            print(f"I'll send it to the server")

            tunnel.send('execute', inp)
        except:
            print('Err')


command_input_thread = Thread(target=command_input)
command_input_thread.start()

# Functions dependent on events


def connect():
    # Change Connection status to True
    app_state.is_connected = True

    # Connection Notification
    print('Connected to Server')

    # Assign hostname as client name
    setname()


def disconnect():
    # Change Connection status to False
    app_state.is_connected = False
    print('disconnected')



# Independent functions

def setname():
    hostname = socket.gethostname()
    tunnel.send('newname', hostname)
