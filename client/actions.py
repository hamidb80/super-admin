from typing import Dict
import os

from provider import states, services
from monkey_patch import print, input

from utils import Messages, events_names as ev
from functions import common_commands


# default events ------------------------------

def connect(data):
    print(Messages.connected)


def reconnect(data=None):
    pass


def disconnect(data):
    print(Messages.disconnected)

# custom events --------------------------------


def hello(data=None):
    print(Messages.hello_from_server)

def auth():
    # check if user has admin privillages
    if states.is_admin:
        print(Messages.you_are_admin)

    else:
        tries = 0

        while tries < 3:
            # input server's password
            entered_pass = input(Messages.enter_pass)
            services.tunnel.send(ev.auth, entered_pass)

            # admin permission
            admin_per = services.tunnel.wait_for(ev.auth_check)

            if admin_per:
                print(Messages.admin_granted)
                states.is_admin = True

                return admin_input()

            # if entered password was wrong
            else:
                print(Messages.wrong_pass)
                tries += 1

        return client_input()


# client input
def client_input():

    while True:
        while states.is_admin is False:

            inp = input(Messages.app_name)

            # print connection status
            if 'status' == inp:
                if states.is_connected:
                    print(Messages.yconnected)

                else:
                    print(Messages.ynotconnected)

            # authenticate
            elif 'auth' == inp:
                return auth()

            elif 'help' == inp:
                print(Messages.client_help)

            else:
                common_commands(inp)


# run commands in client
def admin_input():
    while True:
        while states.is_admin:
            # get user input
            inp = input('Client>')

            if 'exit' in inp:
                print(Messages.exiting_admin)
                services.core.clear_console()
                states.is_admin = False

                return client_input()

            elif 'help' == inp:
                print(Messages.admin_help)

            elif 'online-users' in inp:
                services.tunnel.send(ev.online_users)

                """
                result : [
                    "<client-x>",
                    ...
                ]
                """

                res = services.tunnel.wait_for(ev.online_users_res)

                print(res)

            # send <event> to all users
            # pattern: <event> - data -u / <event> -u
            elif inp[-2:] == '-u':
                command = inp[:-2]

                # try to parse the command
                try:
                    data = None

                    if '-' in command:
                        event, data = command.split('-')
                        data = data.strip()
                    else:
                        event = command

                    event = event.strip()
                except:
                    print(f"can't parse the command")
                    continue

                services.tunnel.send(ev.send_event, dict(
                    event=event,
                    data=data
                ))

            elif inp[-2:] == '-s':
                services.tunnel.send(ev.execute, inp[:-2])
                res = services.tunnel.wait_for(ev.execute_result)

                print(f'result: {res}')

            else:
                common_commands(inp)
