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

                return admin_input()

            # if entered password was wrong
            else:
                services.core.print(Messages.wrong_pass)
                tries += 1

        return client_input()


# client services.core.input
def client_input():

    while True:
        while states.is_admin is False:

            inp = services.core.input(Messages.app_name)

            # services.core.print connection status
            if 'status' == inp:
                if states.is_connected:
                    services.core.print(Messages.yconnected)

                else:
                    services.core.print(Messages.ynotconnected)

            # authenticate
            elif 'auth' == inp:
                return auth()

            elif 'clear' == inp:
                services.core.clear_console()

            elif '' == inp:
                pass

            elif 'help' == inp:
                services.core.print(Messages.client_help)

            else:
                services.core.print(Messages.command_not_defined)


# run commands in client
def admin_input():
    while True:
        while states.is_admin:
            # get user services.core.input
            inp = services.core.input('Client>')

            if 'exit' in inp:
                services.core.print(Messages.exiting_admin)
                services.core.clear_console()
                states.is_admin = False

                return client_input()

            elif inp == '':
                pass

            elif 'clear' == inp:
                services.core.clear_console()

            elif 'help' == inp:
                services.core.print(Messages.admin_help)

            elif inp[-2:] == '-s':
                services.tunnel.send(ev.execute, inp[:-2])
                res = services.tunnel.wait_for(ev.execute_result)

                services.core.print(f'result: {res}')

            else:
                services.core.print(Messages.command_not_defined)


def lock():
    services.core.lock()
