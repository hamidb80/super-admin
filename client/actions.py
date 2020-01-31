from connection import tunnel
from states import app_state
from utils import Password, Colors, cprint, colored
from time import sleep
import socket
import os

from config import APP_NAME

# functions dependant on events


def connect():
    # change connection status to True
    app_state.is_connected = True

    cprint('Connected', Colors.green)

    # send server hostname and new user notification
    connection_initials()


def disconnect():
    # change connection status to False
    app_state.is_connected = False

    # connection notification for admin mode
    if app_state.is_admin:
        cprint('disconnected', Colors.red+Colors.bold)


def auth(data):
    # check if user has admin privillages
    if app_state.is_admin:
        print('You already have admin privillages!', Colors.yellow)

    else:
        tries = 0

        while tries < 3:
            # input server's password
            enteredpass = input("Enter server's password >\n")

            # make a new hash using the entered password and salt
            testhash = Password(enteredpass, data['salt'])

            # compare new hash and the server's hash
            if (testhash.key == data['key']):

                # give admin rights
                cprint('Admin rights granted',
                       Colors.green
                       )

                app_state.is_admin = True
                return client_input()

            # if entered password was wrong
            else:
                cprint('Wrong password!', Colors.red+Colors.bold)
                # send wrong password notification to server
                tunnel.send('notification', {'type': 'wrongpass'})

                tries += 1

            # change main input to False
        app_state.main_input_is_waiting = True


# functions independent from events

# client input
def main_input():

    while True:

        while app_state.is_admin is False and app_state.main_input_is_waiting:

            inp = input(
                colored(f'{APP_NAME} >\n', Colors.blue)
            )

            # authenticate
            if 'auth' in inp:
                ask_auth()

                # change main input status
                app_state.main_input_is_waiting = False

            # print connection status
            elif 'status' in inp:

                if app_state.is_connected:
                    cprint('You are connected', Colors.green)

                else:
                    cprint('You are not connected', Colors.red)
            sleep(0.5)
        sleep(2)


def connection_initials():
    # get hostname
    hostname = socket.gethostname()

    # send hostname and new user notification to server
    tunnel.send('notification', {
                'type': 'connection_initials', 'hostname': hostname})

# ask for authentication from server


def ask_auth():

    # send asked for authentication notification to server
    tunnel.send('notification', {'type': 'askforauth'})

# admin functions

# run commands in client


def client_input():
    while True:
        while app_state.client_is_waiting and app_state.is_admin:
            # get user input
            inp = input('Client >\n')

            # check if user wants to run code in server
            if ' -s' in inp:

                inp = inp.replace(' -s', '')

                print('Sending command', end='')
                cprint(f'{inp} to server', Colors.yellow)

                # send command to server
                tunnel.send('execute', inp)

            elif 'exit' in inp:
                os.system('clear')
                app_state.is_admin = False
                app_state.main_input_is_waiting = True

            else:
                try:
                    exec(inp)
                except:
                    print('Err')
