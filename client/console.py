from typing import Dict
import os

from provider import states, services
from monkey_patch import print, input

from utils import Messages, events_names as ev
from functions import common_commands, remove_first_word, first_word


def client_input():

    while True:
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


def admin_input():
    while states.is_admin:
        # get user input
        inp = input('Client>').strip()
        command = first_word(inp)

        if command in ('quit', 'Q'):
            states.is_admin = False
            print(Messages.exiting_admin)

            return client_input()

        elif 'help' == inp:
            print(Messages.admin_help)

        elif command in ('G', 'get'):
            stuff = remove_first_word(inp)

            val = get_from_server(stuff)
            print(val)

        elif command in ('S', 'send'):
            commnad = remove_first_word(inp)

            send_to_server(commnad)

        elif command in ('E', 'exec'):
            commnad = remove_first_word(inp)

            services.tunnel.send(ev.execute, commnad)
            res = services.tunnel.wait_for(ev.execute_result)

            print(f'result: {res}')

        else:
            common_commands(inp)


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


def get_from_server(stuff: str):
    stuff = stuff.strip()

    if stuff == 'online-users':
        services.tunnel.send(ev.online_users)

        """
        result : [
            "<client-x>",
            ...
        ]
        """

        res = services.tunnel.wait_for(ev.online_users_res)

        return res

    elif stuff == '':
        return 'get what?'

    else:
        return f"'get' commnad for '{stuff}' is not defined"

# pattern: <event> - data -u / <event>


def send_to_server(command: str):
    command = command.strip()

    # try to parse the command
    data = None

    if '-' in command:
        event, data = command.split('-')
        data = data.strip()
    else:
        event = command

    event = command.strip()

    services.tunnel.send(ev.send_event, dict(
        event=event,
        data=data
    ))
