import os
from provider import states, services
from utils import Messages, events_names as ev

from typing import Dict

def connect(data):
    services.core.print(Messages.connected)


def reconnect(data=None):
    pass


def disconnect(data):
    services.core.print(Messages.disconnected)


def hello(data=None):
    services.core.print('server said hello')


def auth():
    # check if user has admin privillages
    if states.is_admin:
        services.core.print(Messages.you_are_admin)

    else:
        tries = 0

        while tries < 3:
            # services.core.input server's password
            entered_pass = services.core.input(Messages.enter_pass)

            services.tunnel.send(ev.auth, entered_pass)

            # admin permission
            admin_per = services.tunnel.wait_for(ev.auth_check)

            if admin_per:
                services.core.print(Messages.admin_granted)
                states.is_admin = True

                return client_input()

            # if entered password was wrong
            else:
                services.core.print(Messages.wrong_pass)
                tries += 1

        return main_input()


# client services.core.input
def main_input():

    while True:

        while states.is_admin is False:

            inp = services.core.input(Messages.app_name)

            # services.core.print connection status
            if 'status' in inp:
                if states.is_connected:
                    services.core.print(Messages.yconnected)

                else:
                    services.core.print(Messages.ynotconnected)

            # authenticate
            elif 'auth' in inp:
                return auth()

            elif 'clear' in inp:
                services.core.clear_console()


# admin functions


# run commands in client
def client_input():
    while True:
        while states.is_admin:
            # get user services.core.input
            inp = services.core.input('Client >\n')

            if inp == 'exit':
                services.core.print(Messages.exiting_admin)
                services.core.clear_console()
                states.is_admin = False

                return main_input()

            elif inp == '':
                pass

            elif inp == 'clear':
                services.core.clear_console()

            # check if user wants to run code in server
            elif inp == 'servermode':
                services.core.print(Messages.running_in_server)

                while True:
                    inp = services.core.input('Server >\n')

                    if inp == 'exit':
                        services.core.print(Messages.running_in_client)
                        break

                    elif inp == '':
                        pass

                    else:
                        services.core.print(f'Sending command {inp} to server')

                        # send command to server
                        services.tunnel.send('execute', inp)
            else:
                try:
                    exec(inp)
                except:
                    services.core.print(Messages.error)


def lock():
    services.core.lock()
