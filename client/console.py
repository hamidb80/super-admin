from typing import Dict
import os

from provider import states, services
from monkey_patch import print, input

from utils.statics import Messages, events_names as ev
from utils.functions import common_commands, remove_first_word, first_word

# TODO: save this into a file
aliases: Dict[str, str] = {}

# --------------------------------------

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
        other_command = remove_first_word(inp)

        if run_admin_commands(command, other_command):
            pass

        elif command in ('quit', 'Q'):
            states.is_admin = False
            print(Messages.exiting_admin)

            return client_input()

        elif 'help' == inp:
            print(Messages.admin_help)

        else:
            common_commands(inp)


def run_admin_commands(command: str, other_command: str) -> bool:
    global aliases

    if command in ('G', 'get'):
        val = get_from_server(other_command)
        print(val)

    elif command in ('S', 'send'):
        send_to_server(other_command)

    elif command in ('E', 'exec'):
        services.tunnel.send(ev.execute, other_command)
        res = services.tunnel.wait_for(ev.execute_result)

        print(f'result: {res}')

    # alias <alias> = <command>
    elif command in ('A', 'alias'):

        try:
            alias, command = [w.strip() for w in other_command.split('=')]
        except:
            print('cannot parse')
        else:
            aliases[alias] = command
            print(f'alias {alias} saved successfully')

    elif command in ('CA', 'call-alias'):
        alias = other_command

        command = first_word(aliases[alias])
        other_command = remove_first_word(aliases[alias])

        run_admin_commands(command, other_command)

    elif command in ('AL', 'alias-list'):
        print(aliases)

    else:
        # it means that the command is not defined in this function
        return False

    return True


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
