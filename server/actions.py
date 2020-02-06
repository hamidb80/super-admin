import os

from driver.models import Client
from utils import set_pass

# set server's password
serverpass = set_pass()

# --- functions dependant on events ---


# user connection notification
def connect(client: Client, data=None):
    print(f'user {client.socket_id} connected')


# user disconnection notification
def disconnect(client: Client, data=None):
    print(f'user {client.name_or_id()} disconnected')

    client.delete()

# get notifications using this function


def notification(client: Client, data):

    # new user notification
    if data['type'] == 'connection_initials':
        client.host_name = data['hostname']
        client.save()

        # announce new name
        print(f'User {client.socket_id} is now called {client.host_name}')

    # wrong password notification
    elif data['type'] == 'wrongpass':
        print(f'User {client.name_or_id()} entered a wrong password')

    # access to server notification
    elif data['type'] == 'hasaccess':
        print(f'User {client.name_or_id()} now has access to server')

    # asking for authentication notification
    elif data['type'] == 'askforauth':

        print(
            f'User {client.name_or_id()} asked for running code in server, sending hashed password and salt.')

        client.send('auth', {'key': serverpass.key, 'salt': serverpass.salt})


# execute command from client with admin privillages
def executefromclient(client: Client, data):
    print(f'User {client.name_or_id()} executed command: {data}')

    try:
        exec(data)
    except:
        print('Err')
