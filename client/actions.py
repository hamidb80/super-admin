from connection import tunnel
from states import app_state
from utils import Password
import socket


# variables


# functions dependant on events

def connect():
    # change Connection status to True
    app_state.is_connected = True
    app_state.is_waiting = True

    # connection Notification
    print('Connected to Server')

    # send newuser event to server
    newuser()


def disconnect():
    # change Connection status to False
    app_state.is_connected = False
    app_state.is_waiting = False
    print('disconnected')


def auth(data):
    enteredpass = input("Please enter server's password\n")
    testhash = Password(enteredpass)

    if (testhash.key == data):
        tunnel.send('has_access', data=None)
        execinserv()

    else:
        print("Wrong Password")
        app_state.is_waiting = True
        tunnel.send('denied_access', data=None)


# functions independant from events

def execinserv():
    inp = input('Server > \n')

    try:
        print(f"I got it: {inp}")
        print(f"I'll send it to the server")

        tunnel.send('execute', inp)
        app_state.is_waiting = True

    except:
        print('Err')


def newuser():
    hostname = socket.gethostname()
    tunnel.send('newuser', hostname)


def ask_auth():
    app_state.is_waiting = False
    tunnel.send('askforauth', data=None)

def command_input():
    while True:
        while app_state.is_waiting==True:
            inp = input('Client >\n')
            try:
                exec(inp)
            except:
                print("Err")
