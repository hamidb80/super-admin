from utils import Password
from driver.models import Client

# TODO: use logger instead of print


# variabales
serverpass = None

# set server's password


def get_pass():
    global serverpass

    passwd = input('Enter Server Password \n')
    serverpass = Password(passwd)
    del passwd


get_pass()

# --- functions dependant on events ---


# user connection notification
def connect(client: Client, data=None):
    print(f'user {client.socket_id} connected')


# user disconnection notification
def disconnect(client: Client, data=None):
    name_or_id = client.socket_id if client.is_unknown else client.host_name
    print(f'user {name_or_id} disconnected')


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

    # illegal command notification
    elif data['type'] == 'illegalcommand':
        print(f'User {client.name_or_id()} attempted to run an illegal command')

    # access to server notification
    elif data['type'] == 'hasaccess':
        print(f'User {client.name_or_id()} now has access to server')

    # asking for authentication notification
    elif data['type'] == 'askforauth':
        print(
            f'User {client.name_or_id()} asked for running code in server, sending hashed password and salt.'
        )

        # client.send('auth', {'key': serverpass.key,'salt': serverpass.salt})
        client.send('auth', {'key': serverpass.key,
                             'salt': serverpass.salt})


# execute command from client with admin privillages
def executefromclient(client: Client, data):
    print(f'User {client.name_or_id()} executed command: {data}')

    try:
        exec(data)
    except:
        print('Err')
