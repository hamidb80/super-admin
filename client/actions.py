from time import sleep
import os
from provider import states
from utils import Password, Messages


# functions dependant on events
def connect(data):
    print(Messages.connected)


def disconnect(data):
    print(Messages.disconnected)


def hello(data=None):
    print('server said hello')


def auth(data):
    # check if user has admin privillages
    if states.is_admin:
        print(Messages.you_are_admin)

    else:
        tries = 0

        while tries < 3:
            # input server's password
            enteredpass = input(Messages.enter_pass)

            # make a new hash using the entered password and salt
            testhash = Password(enteredpass, data['salt'])

            # compare the new hash and the server's hash
            if (testhash.key == data['key']):

                # give admin rights
                print(Messages.admin_granted)

                states.tunnel.send('notification', {'type': 'hasaccess'})

                states.is_admin = True
                return client_input()

            # if entered password was wrong
            else:
                print(Messages.wrong_pass)

                # send wrong password notification to server
                states.tunnel.send('notification', {'type': 'wrongpass'})

                tries += 1

        return main_input()


# ask for authentication from server
def ask_auth():
    # send asked for authentication notification to server
    states.tunnel.send('notification', {'type': 'askforauth'})


# client input
def main_input():

    while True:

        while states.is_admin is False:

            inp = input(Messages.app_name)

            # print connection status
            if 'status' in inp:

                if states.is_connected:
                    print(Messages.yconnected)

                else:
                    print(Messages.ynotconnected)

            # authenticate
            elif 'auth' in inp:
                return ask_auth()

            elif 'clear' in inp:
                os.system('cls')

            sleep(0.5)
        sleep(2)


# admin functions


# run commands in client
def client_input():
    while True:
        while states.is_admin:
            # get user input
            inp = input('Client >\n')

            if inp == 'exit':
                print(Messages.exiting_admin)
                sleep(0.5)
                os.system('cls')
                states.is_admin = False

                return main_input()

            elif inp == '':
                pass

            elif inp == 'clear':
                os.system('cls')

            # check if user wants to run code in server
            elif inp == 'servermode':
                print(Messages.running_in_server)

                while True:
                    inp = input('Server >\n')

                    if inp == 'exit':
                        print(Messages.running_in_client)
                        break

                    elif inp == '':
                        pass

                    else:
                        print(f'Sending command {inp} to server')

                        # send command to server
                        states.tunnel.send('execute', inp)

                    sleep(1)
            else:
                try:
                    exec(inp)
                except:
                    print(Messages.eror)


def lock():
    print('locked')  # for test
    #os.system('rundll32.exe user32.dll,LockWorkStation')
