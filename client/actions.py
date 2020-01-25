from connection import tunnel
from threading import Thread
from states import app_state
from config import Password
import socket


# variables


# Defining command input
def command_input():
    while True:
        inp = input('Client >\n')
        print(f"I got it -{inp}")
        try:
            exec(inp)
        except:
            print("Err")


command_input_thread = Thread(target=command_input)
command_input_thread.start()

# Functions dependent on events


def connect():
    # Change Connection status to True
    app_state.is_connected = True

    # Connection Notification
    print('Connected to Server')

    # send newuser event to server
    newuser()


def disconnect():
    # Change Connection status to False
    app_state.is_connected = False
    print('disconnected')


def auth(data):
    enteredpass = input("Please enter server's password\n")
    testhash = Password(enteredpass)

    if (testhash.key == data):
        tunnel.send('has_access', data=None)
        execinserv()

    else:
        print("Wrong Password")
        tunnel.send('denied_access', data=None)


# Independent functions

def execinserv():
    inp = input('Server > \n')

    try:
        print(f"I got it: {inp}")
        print(f"I'll send it to the server")

        tunnel.send('execute', inp)

    except:
        print('Err')


def newuser():
    hostname = socket.gethostname()
    tunnel.send('newuser', hostname)


def ask_auth():
    tunnel.send('askforauth', data=None)
