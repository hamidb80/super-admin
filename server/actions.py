import os

from driver.models import Client
from utils import Password_Manager

# --- functions dependant on events ---


# user connection notification
async def connect(client: Client, data=None):
    print(f'user {client.socket_id} connected')


# user disconnection notification
async def disconnect(client: Client, data=None):
    print(f'user {client.name_or_id()} disconnected')

    client.delete()

# get notifications using this function


async def notification(client: Client, data):

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

        print(f'User {client.name_or_id()} asked for running code in server, sending hashed password and salt.')

        pass_to_send = Password_Manager.password_list['serverpass']
        await client.send('auth', {'key': pass_to_send.key, 'salt': pass_to_send.salt})


# execute command from client with admin privillages
async def executefromclient(client: Client, data):
    print(f'User {client.name_or_id()} executed command: {data}')

    try:
        exec(data)
    except:
        print('Err')
