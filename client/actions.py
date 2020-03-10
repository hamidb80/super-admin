from time import sleep
import os
from provider import states, services
from utils import Password, Messages


# functions dependant on events
def connect(data):
    services.core.print(Messages.connected)

def reconnect(data=None):
    pass

def disconnect(data):
    services.core.print(Messages.disconnected)


def hello(data=None):
    services.core.print('server said hello')


def auth(data):
    # check if user has admin privillages
    if states.is_admin:
        services.core.print(Messages.you_are_admin)

    else:
        tries = 0

        while tries < 3:
            # services.core.input server's password
            enteredpass = services.core.input(Messages.enter_pass)

            # make a new hash using the entered password and salt
            testhash = Password(enteredpass, data['salt'])

            # compare the new hash and the server's hash
            if (testhash.key == data['key']):

                # give admin rights
                services.core.print(Messages.admin_granted)

                services.tunnel.send('notification', {'type': 'hasaccess'})

                states.is_admin = True
                return client_input()

            # if entered password was wrong
            else:
                services.core.print(Messages.wrong_pass)

                # send wrong password notification to server
                services.tunnel.send('notification', {'type': 'wrongpass'})

                tries += 1

        return main_input()


# ask for authentication from server
def ask_auth():
    # send asked for authentication notification to server
    services.tunnel.send('notification', {'type': 'askforauth'})


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
                return ask_auth()

            elif 'clear' in inp:
                services.core.clear_console()

            sleep(0.5)
        sleep(2)


# admin functions


# run commands in client
def client_input():
    while True:
        while states.is_admin:
            # get user services.core.input
            inp = services.core.input('Client >\n')

            if inp == 'exit':
                services.core.print(Messages.exiting_admin)
                sleep(0.5)
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

                    sleep(1)
            else:
                try:
                    exec(inp)
                except:
                    services.core.print(Messages.eror)


def lock():
    services.core.print('locked')  # for test
    #os.system('rundll32.exe user32.dll,LockWorkStation')
