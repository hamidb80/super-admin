from time import sleep
import socket
import os


from connection import tunnel
from states import app_state
from utils import Password, Messages



# functions dependant on events


def connect():
    # change connection status to True
    app_state.is_connected = True

    print(Messages.connected)

    # send server hostname and new user notification
    connection_initials()


def disconnect():
    # change connection status to False
    app_state.is_connected = False


    print(Messages.disconnected)


def auth(data):
    # check if user has admin privillages
    if app_state.is_admin:
        print(Messages.you_already_have_admin_priv)

    else:
        tries = 0

        while tries < 3:
            # input server's password
            enteredpass = input("Enter server's password >\n")

            # make a new hash using the entered password and salt
            testhash = Password(enteredpass, data['salt'])

            # compare the new hash and the server's hash
            if (testhash.key == data['key']):

                # give admin rights
                print(Messages.admin_rights_granted)

                app_state.is_admin = True
                return client_input()

            # if entered password was wrong
            else:
                print(Messages.wrong_pass)
                
                # send wrong password notification to server
                tunnel.send('notification', {'type': 'wrongpass'})

                tries += 1

        return main_input()


# functions independent from events


# client input
def main_input():

    while True:

        while app_state.is_admin is False:

            inp = input(Messages.app_name)

            # authenticate
            if 'auth' in inp:
                return ask_auth()

            # print connection status
            elif 'status' in inp:

                if app_state.is_connected:
                    print(Messages.you_are_connected)

                else:
                    print(Messages.you_arent_connected)
            
            elif 'clear' in inp:
                os.system('clear')
                
            sleep(0.5)
        sleep(2)


def connection_initials():
    # get hostname
    hostname = socket.gethostname()

    # send hostname and new user notification to server
    tunnel.send('notification', {'type': 'connection_initials', 'hostname': hostname})


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
            if 'servermode' in inp:
                print(Messages.running_in_server)
                
                while True:
                    inp = input('Server >\n')
                    
                    if 'exit' in inp:
                        print(Messages.running_in_client)
                        break
                    
                    elif inp=='':
                        pass
                    
                    else:
                        print('Sending command',Messages.input(inp), 'to server')
                    
                        # send command to server
                        tunnel.send('execute', inp)
                    
                    sleep(1)                
                                     
            elif 'exit' in inp:
                print(Messages.exiting_admin)
                sleep(0.3)
                
                os.system('clear')
                app_state.is_admin = False
                
                return main_input()

            else:
                try:
                    exec(inp)
                except:
                    print('Err')
